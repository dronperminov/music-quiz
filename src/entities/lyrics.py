from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class LyricsLine:
    time: float
    text: str

    def to_dict(self) -> dict:
        return {"time": self.time, "text": self.text}

    @classmethod
    def from_dict(cls: "LyricsLine", data: dict) -> "LyricsLine":
        return cls(time=data["time"], text=data["text"])


@dataclass
class Lyrics:
    lines: List[LyricsLine]
    chorus: List[Tuple[int, int]]

    def to_dict(self) -> dict:
        return {
            "lines": [line.to_dict() for line in self.lines],
            "chorus": [[start, end] for start, end in self.chorus]
        }

    @classmethod
    def from_dict(cls: "Lyrics", data: dict) -> "Lyrics":
        return cls(
            lines=[LyricsLine.from_dict(line) for line in data["lines"]],
            chorus=[(start, end) for start, end in data["chorus"]]
        )
