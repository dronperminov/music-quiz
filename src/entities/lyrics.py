import re
from dataclasses import dataclass
from typing import List, Tuple

from src.entities.chorus_detector import ChorusDetector
from src.entities.lyrics_line import LyricsLine
from src.enums import Language


@dataclass
class Lyrics:
    lines: List[LyricsLine]
    chorus: List[Tuple[int, int]]
    lrc: bool

    @classmethod
    def from_lrc(cls: "Lyrics", lyrics_str: str) -> "Lyrics":
        lines = []

        for line in lyrics_str.split("\n"):
            if (lyrics_line := LyricsLine.from_lrc(lrc_line=line)).text:
                lines.append(lyrics_line)

        return Lyrics(lines=lines, chorus=ChorusDetector().detect(lines), lrc=True)

    @classmethod
    def from_text(cls: "Lyrics", text: str) -> "Lyrics":
        lines = [LyricsLine(time=0, text=line.strip()) for line in text.split("\n") if line.strip()]
        return Lyrics(lines=lines, chorus=ChorusDetector().detect(lines), lrc=False)

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
