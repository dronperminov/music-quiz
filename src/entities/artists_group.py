import random
from dataclasses import dataclass
from typing import List

from src.entities.metadata import Metadata
from src.entities.track import Track


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

    def get_diff(self, data: dict) -> dict:
        group_data = self.to_dict()
        diff = {}

        for field in ["name", "description", "artist_ids", "image_url"]:
            if field in data and group_data[field] != data[field]:
                diff[field] = {"prev": group_data[field], "new": data[field]}

        return diff

    def get_variants(self, track: Track, max_variants: int) -> List[int]:
        if len(self.artist_ids) <= max_variants:
            variants = [artist_id for artist_id in self.artist_ids]
        else:
            correct = [artist_id for artist_id in track.artists if artist_id in self.artist_ids]
            assert len(correct) == 1
            incorrect = [artist_id for artist_id in self.artist_ids if artist_id not in correct]
            variants = correct + random.sample(incorrect, k=max_variants - 1)

        random.shuffle(variants)
        return variants

    def remove_artist(self, artist_id: int) -> None:
        self.artist_ids = [group_artist_id for group_artist_id in self.artist_ids if group_artist_id != artist_id]

    def add_artist(self, artist_id: int) -> None:
        if artist_id in self.artist_ids:
            return

        self.artist_ids.append(artist_id)
