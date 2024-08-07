from dataclasses import dataclass
from typing import Dict, List

from src.entities.metadata import Metadata
from src.entities.source import Source
from src.enums import ArtistType, Genre


@dataclass
class Artist:
    artist_id: int
    source: Source
    name: str
    description: str
    artist_type: ArtistType
    image_urls: List[str]
    listen_count: int
    tracks: Dict[int, int]
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
            "tracks": self.get_tracks_dict(),
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
            tracks={track["track_id"]: track["position"] for track in data["tracks"]},
            genres=[Genre(genre) for genre in data["genres"]],
            metadata=Metadata.from_dict(data["metadata"])
        )

    def get_tracks_dict(self) -> List[dict]:
        return [{"track_id": track_id, "position": position} for track_id, position in self.tracks.items()]

    def get_diff(self, data: dict) -> dict:
        artist_data = self.to_dict()
        diff = {}

        for field in ["name", "description", "artist_type", "image_urls", "listen_count", "genres"]:
            if field in data and artist_data[field] != data[field]:
                diff[field] = {"prev": artist_data[field], "new": data[field]}

        if "tracks" in data:
            artist_tracks = sorted(artist_data["tracks"], key=lambda track: track["track_id"])
            data_tracks = sorted(data["tracks"], key=lambda track: track["track_id"])

            if artist_tracks != data_tracks:
                diff["tracks"] = {"prev": artist_data["tracks"], "new": data["tracks"]}

        return diff
