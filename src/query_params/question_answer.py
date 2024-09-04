from dataclasses import dataclass
from typing import Optional


@dataclass
class QuestionAnswer:
    correct: bool
    answer_time: Optional[float]
    group_id: Optional[int] = None


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
