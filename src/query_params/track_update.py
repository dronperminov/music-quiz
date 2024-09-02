from dataclasses import dataclass
from typing import Optional

from src.entities.lyrics import Lyrics
from src.entities.track import Track
from src.enums import Language


@dataclass
class TrackUpdate:
    track_id: int
    language: Optional[Language] = None
    year: Optional[int] = None
    validated: Optional[bool] = None

    def to_data(self, lyrics: Optional[Lyrics]) -> dict:
        data = {}

        if self.language:
            data["language"] = self.language.value

        if self.year:
            data["year"] = self.year

        if self.validated is not None and lyrics:
            data["lyrics"] = lyrics.to_dict()
            data["lyrics"]["validated"] = self.validated

        return data
