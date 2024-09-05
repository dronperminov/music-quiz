from dataclasses import dataclass
from typing import Optional


@dataclass
class QuestionAnswer:
    correct: bool
    answer_time: Optional[float]
    group_id: Optional[int] = None

    @classmethod
    def from_dict(cls: "QuestionAnswer", data: dict) -> "QuestionAnswer":
        return cls(correct=data["correct"], answer_time=data["answer_time"], group_id=data.get("group_id", None))

    def to_dict(self) -> dict:
        answer = {"correct": self.correct, "answer_time": self.answer_time}

        if self.group_id:
            answer["group_id"] = self.group_id

        return answer


@dataclass
class QuizTourQuestionAnswer:
    question_id: int
    correct: bool
    answer_time: float


@dataclass
class MultiPlayerQuestionAnswer:
    session_id: str
    correct: bool
    answer_time: Optional[float]
    group_id: Optional[int] = None
