from dataclasses import dataclass
from typing import List, Optional

from src.entities.lyrics import Lyrics
from src.entities.metadata import Metadata
from src.entities.source import Source
from src.enums import Genre, Language


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
    image_urls: List[str]
    metadata: Metadata

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
            "image_urls": self.image_urls,
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
            image_urls=data["image_urls"],
            metadata=Metadata.from_dict(data["metadata"])
        )

    def get_diff(self, data: dict) -> dict:
        track_data = self.to_dict()
        diff = {}

        for field in ["title", "artists", "year", "lyrics", "genres", "language", "duration", "downloaded", "image_urls"]:
            if field in data and track_data[field] != data[field]:
                diff[field] = {"prev": track_data[field], "new": data[field]}

        return diff
