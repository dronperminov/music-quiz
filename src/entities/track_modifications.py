from dataclasses import dataclass


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
