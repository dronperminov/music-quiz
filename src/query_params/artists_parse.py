from dataclasses import dataclass
from typing import List


@dataclass
class ArtistsParse:
    artist_ids: List[str]
    max_tracks: int = 20
    max_artists: int = 4
    from_playlist: bool = True
