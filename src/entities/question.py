from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.entities.track_modifications import TrackModifications
from src.enums import QuestionType


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
            timestamp=data["timestamp"]
        )
