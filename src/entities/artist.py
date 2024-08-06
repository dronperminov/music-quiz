from dataclasses import dataclass
from typing import Dict, List

from bson import ObjectId

from src.entities.metadata import Metadata
from src.entities.source import Source
from src.enums import ArtistType, Genre


@dataclass
class Artist:
    artist_id: ObjectId
    source: Source
    name: str
    description: str
    artist_type: ArtistType
    image_urls: List[str]
    listen_count: int
    tracks: Dict[ObjectId, int]
    genres: List[Genre]
    metadata: Metadata

    def to_dict(self) -> dict:
        return {
            "artist_id": self.artist_id,
            "source": self.source.to_dict(),
            "name": self.name,
            "description": self.description,
            "artist_type": self.artist_type.value,
            "image_urls": self.image_urls,
            "listen_count": self.listen_count,
            "tracks": self.tracks,
            "genres": [genre.value for genre in self.genres],
            "metadata": self.metadata.to_dict()
        }

    @classmethod
    def from_dict(cls: "Artist", data: dict) -> "Artist":
        return cls(
            artist_id=data["artist_id"],
            source=Source.from_dict(data["source"]),
            name=data["name"],
            description=data["description"],
            artist_type=ArtistType(data["artist_type"]),
            image_urls=data["image_urls"],
            listen_count=data["listen_count"],
            tracks=data["tracks"],
            genres=[Genre(genre) for genre in data["genres"]],
            metadata=Metadata.from_dict(data["metadata"])
        )
