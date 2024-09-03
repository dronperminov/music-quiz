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
    tracks_count: int
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
            "tracks_count": self.tracks_count,
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
            tracks_count=data["tracks_count"],
            genres=[Genre(genre) for genre in data["genres"]],
            metadata=Metadata.from_dict(data["metadata"])
        )

    def get_tracks_dict(self) -> List[dict]:
        return [{"track_id": track_id, "position": position} for track_id, position in self.tracks.items()]

    def get_diff(self, data: dict, from_yandex: bool = False) -> dict:
        artist_data = self.to_dict()
        diff = {}

        fields = ["name", "description", "image_urls", "listen_count", "tracks_count"]

        if not from_yandex:
            fields.append("genres")

        for field in fields:
            if field in data and artist_data[field] != data[field]:
                diff[field] = {"prev": artist_data[field], "new": data[field]}

        if not from_yandex and "artist_type" in data and artist_data["artist_type"] != data["artist_type"] and data["artist_type"] != ArtistType.UNKNOWN.value:
            diff["artist_type"] = {"prev": artist_data["artist_type"], "new": data["artist_type"]}

        if "tracks" in data:
            artist_tracks = sorted(artist_data["tracks"], key=lambda track: track["track_id"])
            data_tracks = sorted(data["tracks"], key=lambda track: track["track_id"])

            if artist_tracks != data_tracks:
                diff["tracks"] = {"prev": artist_data["tracks"], "new": data["tracks"]}

        return diff

    def format_listen_count(self) -> str:
        if self.listen_count >= 1000000:
            return f"{self.listen_count / 1000000:.2f}M"

        if self.listen_count >= 1000:
            return f"{self.listen_count / 1000:.2f}K"

        return str(self.listen_count)

    def get_image_url(self) -> str:
        return self.image_urls[0] if self.image_urls else "/images/artists/default.png"
