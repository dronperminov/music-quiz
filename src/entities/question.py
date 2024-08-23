import random
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from src.entities.artist import Artist
from src.entities.settings import Settings
from src.entities.track import Track
from src.entities.track_modifications import TrackModifications
from src.enums import QuestionType
from src.query_params.question_answer import QuestionAnswer


@dataclass
class Question:
    username: str
    question_type: QuestionType
    group_id: Optional[int]
    track_id: int
    title: str
    answer: str
    question_timecode: str
    question_seek: float
    answer_seek: Optional[float]
    track_modifications: TrackModifications
    correct: Optional[bool]
    answer_time: Optional[float]
    timestamp: datetime

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "question_type": self.question_type.value,
            "group_id": self.group_id,
            "track_id": self.track_id,
            "title": self.title,
            "answer": self.answer,
            "question_timecode": self.question_timecode,
            "question_seek": self.question_seek,
            "answer_seek": self.answer_seek,
            "track_modifications": self.track_modifications.to_dict(),
            "correct": self.correct,
            "answer_time": self.answer_time,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls: "Question", data: dict) -> "Question":
        return cls(
            username=data["username"],
            question_type=QuestionType(data["question_type"]),
            group_id=data.get("group_id", None),
            track_id=data["track_id"],
            title=data["title"],
            answer=data["answer"],
            question_timecode=data["question_timecode"],
            question_seek=data["question_seek"],
            answer_seek=data["answer_seek"],
            track_modifications=TrackModifications.from_dict(data["track_modifications"]),
            correct=data["correct"],
            answer_time=data["answer_time"],
            timestamp=data["timestamp"]
        )

    def init_base(self, question_type: QuestionType, settings: Settings, track_id: int, group_id: Optional[int]) -> None:
        self.question_type = question_type
        self.username = settings.username
        self.group_id = group_id
        self.track_id = track_id

        self.track_modifications = TrackModifications.from_settings(settings.question_settings.track_modifications)
        self.remove_answer()

    def set_answer(self, answer: QuestionAnswer) -> None:
        self.correct = answer.correct
        self.answer_time = answer.answer_time
        self.timestamp = datetime.now()

    def remove_answer(self) -> None:
        self.correct = None
        self.answer_time = None
        self.timestamp = datetime.now()

    def get_artist_types(self, track: Track, artist_id2artist: Dict[int, Artist], simple: bool) -> str:
        artist_types = [artist_id2artist[artist_id].artist_type.to_title(simple=simple) for artist_id in track.artists]

        if len(artist_types) == 1:
            return artist_types[0]

        return f'{", ".join(artist_types[:-1])} и {artist_types[-1]}'

    def get_random_seek(self, track: Track, start_from_chorus: bool) -> float:
        if track.lyrics and track.lyrics.lrc:
            if start_from_chorus and track.lyrics.chorus:
                start, end = random.choice(track.lyrics.chorus)
                return track.lyrics.lines[start].time

            line = random.choice(track.lyrics.lines[:len(track.lyrics) * 3 // 4])
            return line.time

        if track.duration > 0:
            return round(random.random() * track.duration * 0.75, 2)

        return 0
