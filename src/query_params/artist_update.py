from dataclasses import dataclass
from typing import List, Optional

from src.enums import ArtistType, Genre


@dataclass
class ArtistUpdate:
    artist_id: int
    artist_type: Optional[ArtistType] = None
    genres: Optional[List[Genre]] = None
    update_tracks: Optional[bool] = None

    def to_data(self) -> dict:
        data = {}

        if self.artist_type:
            data["artist_type"] = self.artist_type.value

        if self.genres:
            data["genres"] = [genre.value for genre in self.genres]

        return data
