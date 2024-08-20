from dataclasses import dataclass
from typing import List, Optional

from src.entities.lyrics import Lyrics
from src.entities.metadata import Metadata
from src.entities.source import Source
from src.enums import Genre, Language, QuestionType
from src.enums.question_type import INTRO_MIN_TIME


@dataclass
class Track:
    track_id: int
    source: Source
    title: str
    artists: List[int]
    year: int
    lyrics: Optional[Lyrics]
    genres: List[Genre]
    language: Language
    duration: float
    downloaded: bool
    image_url: Optional[str]
    metadata: Metadata

    @property
    def artists_count(self) -> str:
        return "solo" if len(self.artists) == 1 else "feat"

    def to_dict(self) -> dict:
        return {
            "track_id": self.track_id,
            "source": self.source.to_dict(),
            "title": self.title,
            "artists": self.artists,
            "year": self.year,
            "lyrics": self.lyrics.to_dict() if self.lyrics else None,
            "genres": [genre.value for genre in self.genres],
            "language": self.language.value,
            "duration": self.duration,
            "downloaded": self.downloaded,
            "image_url": self.image_url,
            "metadata": self.metadata.to_dict()
        }

    @classmethod
    def from_dict(cls: "Track", data: dict) -> "Track":
        return cls(
            track_id=data["track_id"],
            source=Source.from_dict(data["source"]),
            title=data["title"],
            artists=data["artists"],
            year=data["year"],
            lyrics=Lyrics.from_dict(data["lyrics"]) if data["lyrics"] else None,
            genres=[Genre(genre) for genre in data["genres"]],
            language=Language(data["language"]),
            duration=data["duration"],
            downloaded=data["downloaded"],
            image_url=data["image_url"],
            metadata=Metadata.from_dict(data["metadata"])
        )

    def get_diff(self, data: dict) -> dict:
        track_data = self.to_dict()
        diff = {}

        for field in ["title", "artists", "year", "lyrics", "genres", "language", "duration", "downloaded", "image_url"]:
            if field in data and track_data[field] != data[field]:
                diff[field] = {"prev": track_data[field], "new": data[field]}

        return diff

    def format_duration(self) -> str:
        seconds = round(self.duration)
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def get_question_types(self) -> List[QuestionType]:
        question_types = [QuestionType.ARTIST_BY_TRACK, QuestionType.NAME_BY_TRACK]

        if not self.lyrics or not self.lyrics.lrc:
            return question_types

        question_types.append(QuestionType.LINE_BY_TEXT)

        if self.lyrics.lines[0].time > INTRO_MIN_TIME:
            question_types.append(QuestionType.ARTIST_BY_INTRO)

        if self.lyrics.chorus:
            question_types.append(QuestionType.LINE_BY_CHORUS)

        return question_types
