import random
from typing import Optional

from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track


class NameByTrackQuestion(Question):
    def __init__(self, track: Track, settings: Settings, group_id: Optional[int] = None) -> None:
        self.init_base(settings=settings, track_id=track.track_id, group_id=group_id)

        self.title = "Назовите название трека"
        self.answer = track.title

        self.question_timecode = ""
        self.question_seek = self.__get_question_seek(track)
        self.answer_seek = None

    def __get_question_seek(self, track: Track) -> float:
        if track.lyrics is None or not track.lyrics.lrc:
            return 0

        line = random.choice(track.lyrics.lines[:len(track.lyrics) * 3 // 4])
        return line.time
