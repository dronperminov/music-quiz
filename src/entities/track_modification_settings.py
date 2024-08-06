from dataclasses import dataclass


@dataclass
class TrackModificationSettings:
    change_playback_rate: bool
    probability: float

    def to_dict(self) -> dict:
        return {
            "change_playback_rate": self.change_playback_rate,
            "probability": self.probability
        }

    @classmethod
    def from_dict(cls: "TrackModificationSettings", data: dict) -> "TrackModificationSettings":
        return cls(
            change_playback_rate=data["change_playback_rate"],
            probability=data["probability"]
        )
