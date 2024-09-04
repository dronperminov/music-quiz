from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from src.entities.question import Question
from src.query_params.question_answer import QuestionAnswer


@dataclass
class Session:
    session_id: str
    players: List[str]
    answers: Dict[str, QuestionAnswer]
    created_at: datetime
    created_by: str
    question: Optional[Question]

    @classmethod
    def from_dict(cls: "Session", data: dict) -> "Session":
        return cls(
            session_id=data["session_id"],
            players=data["players"],
            answers={username: QuestionAnswer(correct=answer["correct"], answer_time=answer["answer_time"]) for username, answer in data["answers"].items()},
            created_at=data["created_at"],
            created_by=data["created_by"],
            question=Question.from_dict(data["question"]) if data["question"] else None
        )

    @classmethod
    def create(cls: "Session", session_id: str, username: str) -> "Session":
        return cls(
            session_id=session_id,
            players=[username],
            answers={},
            created_at=datetime.now(),
            created_by=username,
            question=None
        )

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "players": self.players,
            "answers": {username: {"correct": answer.correct, "answer_time": answer.answer_time} for username, answer in self.answers.items()},
            "created_at": self.created_at,
            "created_by": self.created_by,
            "question": self.question.to_dict() if self.question else None
        }

    def set_question(self, question: Question) -> None:
        self.question = question
        self.answers = {}

    def all_answered(self) -> bool:
        for username in self.players:
            if username not in self.answers:
                return False

        return True
