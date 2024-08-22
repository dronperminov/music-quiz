from dataclasses import dataclass
from typing import Optional

from src.enums import Language


@dataclass
class TrackUpdate:
    track_id: int
    language: Optional[Language]

    def to_data(self) -> dict:
        data = {}

        if self.language:
            data["language"] = self.language.value

        return data
