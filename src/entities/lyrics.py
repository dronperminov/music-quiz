import re
from dataclasses import dataclass
from typing import List, Tuple

from src.enums import Language


@dataclass
class LyricsLine:
    time: float
    text: str

    def to_dict(self) -> dict:
        return {"time": self.time, "text": self.text}

    @classmethod
    def from_dict(cls: "LyricsLine", data: dict) -> "LyricsLine":
        return cls(time=data["time"], text=data["text"])

    @classmethod
    def from_lrc(cls: "LyricsLine", lrc_line: str) -> "LyricsLine":
        match = re.search(r"^\[(?P<minute>\d+):(?P<second>\d+\.\d+)] (?P<text>.*)$", lrc_line)
        text, minute, second = match.group("text").strip(), float(match.group("minute")), float(match.group("second"))
        return LyricsLine(time=round(minute * 60 + second, 2), text=text)


@dataclass
class Lyrics:
    lines: List[LyricsLine]
    chorus: List[Tuple[int, int]]
    lrc: bool

    @classmethod
    def from_lrc(cls: "Lyrics", lyrics_str: str) -> "Lyrics":
        lyrics_lines = []

        for line in lyrics_str.split("\n"):
            if (lyrics_line := LyricsLine.from_lrc(lrc_line=line)).text:
                lyrics_lines.append(lyrics_line)

        return Lyrics(lines=lyrics_lines, chorus=[], lrc=True)  # TODO: detect chorus

    @classmethod
    def from_text(cls: "Lyrics", text: str) -> "Lyrics":
        lines = [LyricsLine(time=0, text=line) for line in text.split("\n")]
        return Lyrics(lines=lines, chorus=[], lrc=False)

    def to_dict(self) -> dict:
        return {
            "lines": [line.to_dict() for line in self.lines],
            "chorus": [[start, end] for start, end in self.chorus],
            "lrc": self.lrc
        }

    @classmethod
    def from_dict(cls: "Lyrics", data: dict) -> "Lyrics":
        return cls(
            lines=[LyricsLine.from_dict(line) for line in data["lines"]],
            chorus=[(start, end) for start, end in data["chorus"]],
            lrc=data["lrc"]
        )

    def get_text(self) -> str:
        return "\n".join(line.text for line in self.lines)

    def get_language(self) -> Language:
        text = self.get_text()

        if len(re.findall(r"[а-яА-ЯёЁ]", text)) > 10:
            return Language.RUSSIAN

        if len(re.findall(r"[a-zA-Z]", text)) > len(text) * 0.4:
            return Language.FOREIGN

        return Language.UNKNOWN
