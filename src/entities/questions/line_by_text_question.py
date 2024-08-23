from typing import Dict, Optional

from src.entities.artist import Artist
from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track
from src.enums import QuestionType


class LineByTextQuestion(Question):
    def __init__(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings, group_id: Optional[int] = None) -> None:
        self.init_base(question_type=QuestionType.LINE_BY_TEXT, settings=settings, track_id=track.track_id, group_id=group_id)

        self.title = "Продолжите строку"
        self.answer = ""

        self.question_timecode = ""
        self.question_seek = self.get_random_seek(track, settings.question_settings.start_from_chorus)
        self.answer_seek = None
