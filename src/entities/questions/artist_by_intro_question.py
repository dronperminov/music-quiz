from typing import Dict, Optional

from src.entities.artist import Artist
from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track
from src.enums import QuestionType


class ArtistByIntroQuestion(Question):
    def __init__(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings, group_id: Optional[int] = None) -> None:
        self.init_base(question_type=QuestionType.ARTIST_BY_INTRO, settings=settings, track_id=track.track_id, group_id=group_id)

        self.title = f"Назовите {self.get_artist_types(track, artist_id2artist, settings.question_settings.show_simple_artist_type)}"
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)

        self.question_timecode = f"0,{round(track.lyrics.lines[0].time - 1, 2)}"
        self.question_seek = 0
        self.answer_seek = None
