from dataclasses import dataclass
from typing import Optional


@dataclass
class QuestionAnswer:
    correct: bool
    answer_time: Optional[float]
    group_id: Optional[int]
