from dataclasses import dataclass
from typing import List


@dataclass
class GroupTracksAnalytics:
    total: int
    listened: int
    correct: int
    incorrect: int
    unknown: int

    def __post_init__(self) -> None:
        total = max(self.listened, 1)
        self.correct_percents = self.correct / total * 100
        self.incorrect_percents = self.incorrect / total * 100
        self.unknown_percents = self.unknown / total * 100

    @classmethod
    def evaluate(cls: "GroupTracksAnalytics", questions: List[dict], tracks: List[dict]) -> "GroupTracksAnalytics":
        listened_track_ids = {question["track_id"] for question in questions}
        correct = set()
        incorrect = set()

        for question in questions:
            if question["correct"]:
                correct.add(question["track_id"])
            else:
                incorrect.add(question["track_id"])

        unknown = correct.intersection(incorrect)
        correct = correct.difference(unknown)
        incorrect = incorrect.difference(unknown)

        return cls(
            total=len(tracks),
            listened=len(listened_track_ids),
            correct=len(correct),
            incorrect=len(incorrect),
            unknown=len(unknown)
        )
