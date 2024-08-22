from dataclasses import dataclass
from typing import Optional

from src.enums import ArtistType


@dataclass
class ArtistUpdate:
    artist_id: int
    artist_type: Optional[ArtistType]

    def to_data(self) -> dict:
        data = {}

        if self.artist_type:
            data["artist_type"] = self.artist_type.value

        return data
