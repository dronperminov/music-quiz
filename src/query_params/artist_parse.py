from dataclasses import dataclass


@dataclass
class ArtistParse:
    artist_id: str
    max_tracks: int = 20
    max_artists: int = 4
