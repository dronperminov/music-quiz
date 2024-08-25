from dataclasses import dataclass
from typing import Optional

from src.entities.note import Note


@dataclass
class NoteTrackUpdate:
    track_id: int
    seek: float


@dataclass
class NoteUpdate:
    artist_id: int
    text: Optional[str] = None
    track: Optional[NoteTrackUpdate] = None

    def to_note(self, username: str) -> Note:
        text = self.text if self.text else ""
        track_id2seek = {self.track.track_id: self.track.seek} if self.track else {}
        return Note(username=username, artist_id=self.artist_id, text=text, track_id2seek=track_id2seek)
