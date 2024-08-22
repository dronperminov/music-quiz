from typing import Optional

from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track
from src.enums import QuestionType


class NameByTrackQuestion(Question):
    def __init__(self, track: Track, settings: Settings, group_id: Optional[int] = None) -> None:
        self.init_base(question_type=QuestionType.NAME_BY_TRACK, settings=settings, track_id=track.track_id, group_id=group_id)

        self.title = "Назовите название трека"
        self.answer = track.title

        self.question_timecode = ""
        self.question_seek = self.get_random_seek(track, settings.question_settings.start_from_chorus)
        self.answer_seek = None
