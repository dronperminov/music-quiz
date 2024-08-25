from dataclasses import dataclass
from typing import Dict


@dataclass
class Note:
    username: str
    artist_id: int
    text: str
    track_id2seek: Dict[int, float]

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "artist_id": self.artist_id,
            "text": self.text,
            "track_id2seek": [{"track_id": track_id, "seek": seek} for track_id, seek in self.track_id2seek.items()]
        }

    @classmethod
    def from_dict(cls: "Note", data: dict) -> "Note":
        return cls(
            username=data["username"],
            artist_id=data["artist_id"],
            text=data["text"],
            track_id2seek={track_seek["track_id"]: track_seek["seek"] for track_seek in data["track_id2seek"]}
        )

    def get_diff(self, data: dict) -> dict:
        note_data = self.to_dict()
        diff = {}

        for field in ["text", "track_id2seek"]:
            if field in data and note_data[field] != data[field]:
                diff[field] = {"prev": note_data[field], "new": data[field]}

        return diff

    def update_track(self, track_id: int, seek: int) -> None:
        if track_id in self.track_id2seek:
            self.track_id2seek.pop(track_id)
        else:
            self.track_id2seek[track_id] = seek
