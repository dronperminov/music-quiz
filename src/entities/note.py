from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Union


@dataclass
class Note:
    username: str
    artist_id: int
    text: str
    track_id2seek: Dict[int, float]
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "artist_id": self.artist_id,
            "text": self.text,
            "track_id2seek": [{"track_id": track_id, "seek": seek} for track_id, seek in self.track_id2seek.items()],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls: "Note", data: dict) -> "Note":
        return cls(
            username=data["username"],
            artist_id=data["artist_id"],
            text=data["text"],
            track_id2seek={track_seek["track_id"]: track_seek["seek"] for track_seek in data["track_id2seek"]},
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )

    def get_diff(self, data: dict) -> dict:
        note_data = self.to_dict()
        diff = {}

        for field in ["text", "track_id2seek"]:
            if field in data and note_data[field] != data[field]:
                diff[field] = {"prev": note_data[field], "new": data[field]}

        return diff

    def get_order_key(self, order: str) -> Union[str, int, datetime]:
        if order == "tracks_count":
            return len(self.track_id2seek)

        if order == "created_at":
            return self.created_at

        if order == "updated_at":
            return self.updated_at

        return self.artist_id

    def update_track(self, track_id: int, seek: int) -> None:
        if track_id in self.track_id2seek:
            self.track_id2seek.pop(track_id)
        else:
            self.track_id2seek[track_id] = seek
