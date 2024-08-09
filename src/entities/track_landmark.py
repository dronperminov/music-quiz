from dataclasses import dataclass


@dataclass
class TrackLandmark:
    track_id: int
    timecode: str
    text: str

    def to_json(self) -> dict:
        return {
            "track_id": self.track_id,
            "timecode": self.timecode,
            "text": self.text
        }

    @classmethod
    def from_dict(cls: "TrackLandmark", data: dict) -> "TrackLandmark":
        return cls(
            track_id=data["track_id"],
            timecode=data["timecode"],
            text=data["text"]
        )
