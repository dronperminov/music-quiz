from dataclasses import dataclass
from typing import List

from src.entities.metadata import Metadata


@dataclass
class ArtistsGroup:
    group_id: int
    name: str
    description: str
    artist_ids: List[int]
    image_url: str
    metadata: Metadata

    def to_dict(self) -> dict:
        return {
            "group_id": self.group_id,
            "name": self.name,
            "description": self.description,
            "artist_ids": self.artist_ids,
            "image_url": self.image_url,
            "metadata": self.metadata.to_dict()
        }

    @classmethod
    def from_dict(cls: "ArtistsGroup", data: dict) -> "ArtistsGroup":
        return cls(
            group_id=data["group_id"],
            name=data["name"],
            description=data["description"],
            artist_ids=data["artist_ids"],
            image_url=data["image_url"],
            metadata=Metadata.from_dict(data["metadata"])
        )
