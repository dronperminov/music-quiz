from dataclasses import dataclass
from typing import Optional

from src.enums import Language


@dataclass
class TrackUpdate:
    track_id: int
    language: Optional[Language] = None
    year: Optional[int] = None

    def to_data(self) -> dict:
        data = {}

        if self.language:
            data["language"] = self.language.value

        if self.year:
            data["year"] = self.year

        return data
