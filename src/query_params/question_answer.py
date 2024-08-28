from dataclasses import dataclass
from typing import Optional


@dataclass
class QuestionAnswer:
    correct: bool
    answer_time: Optional[float]
    group_id: Optional[int]


@dataclass
class QuizTourQuestionAnswer:
    question_id: int
    correct: bool
    answer_time: float
