import random
from dataclasses import dataclass

from src.entities.track_modification_settings import TrackModificationSettings


@dataclass
class TrackModifications:
    playback_rate: float

    def to_dict(self) -> dict:
        return {
            "playback_rate": self.playback_rate
        }

    @classmethod
    def from_dict(cls: "TrackModifications", data: dict) -> "TrackModifications":
        return cls(
            playback_rate=data["playback_rate"]
        )

    @classmethod
    def from_settings(cls: "TrackModifications", settings: TrackModificationSettings) -> "TrackModifications":
        if random.random() < settings.probability:
            return cls(playback_rate=random.choice([0.25, 0.5, 0.75, 1.5, 2, 3, 4]))

        return cls(playback_rate=1)
