from dataclasses import dataclass
from typing import List, Optional

from src.entities.lyrics import Lyrics
from src.enums import Language


@dataclass
class TrackUpdate:
    track_id: int
    language: Optional[Language] = None
    year: Optional[int] = None
    validated: Optional[bool] = None
    chorus: Optional[List[List[int]]] = None

    def to_data(self, lyrics: Optional[Lyrics]) -> dict:
        data = {}

        if self.language:
            data["language"] = self.language.value

        if self.year:
            data["year"] = self.year

        if lyrics:
            data["lyrics"] = lyrics.to_dict()

        if self.validated is not None:
            data["lyrics"]["validated"] = self.validated

        if self.chorus is not None:
            data["lyrics"]["chorus"] = self.chorus

        return data
