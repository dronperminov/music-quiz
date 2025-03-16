from dataclasses import dataclass


@dataclass
class PlaylistParse:
    playlist_id: str
    playlist_username: str
    max_tracks: int
