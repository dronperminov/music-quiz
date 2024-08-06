from dataclasses import dataclass
from typing import List

from bson import ObjectId

from src.entities.track_landmark import TrackLandmark


@dataclass
class Note:
    username: str
    artist_id: ObjectId
    text: str
    track_landmarks: List[TrackLandmark]

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "artist_id": self.artist_id,
            "text": self.text,
            "track_landmarks": [track_landmark.to_json() for track_landmark in self.track_landmarks]
        }

    @classmethod
    def from_dict(cls: "Note", data: dict) -> "Note":
        return cls(
            username=data["username"],
            artist_id=data["artist_id"],
            text=data["text"],
            track_landmarks=[TrackLandmark.from_dict(track_landmark) for track_landmark in data["track_landmarks"]]
        )
