from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GroupArtistsAnalytics:
    correct: Dict[int, int]
    incorrect: Dict[int, int]
    unknown: Dict[int, int]
    unlistened: Dict[int, int]
    total: Dict[int, int]

    def __post_init__(self) -> None:
        self.correct_percents = {artist_id: count / max(self.total[artist_id], 1) * 100 for artist_id, count in self.correct.items()}
        self.incorrect_percents = {artist_id: count / max(self.total[artist_id], 1) * 100 for artist_id, count in self.incorrect.items()}
        self.unknown_percents = {artist_id: count / max(self.total[artist_id], 1) * 100 for artist_id, count in self.unknown.items()}
        self.unlistened_percents = {artist_id: count / max(self.total[artist_id], 1) * 100 for artist_id, count in self.unlistened.items()}

    @classmethod
    def evaluate(cls: "GroupArtistsAnalytics", artist_ids: List[int], questions: List[dict], tracks: List[dict]) -> "GroupArtistsAnalytics":
        track_id2track = {track["track_id"]: track for track in tracks}

        correct = {artist_id: set() for artist_id in artist_ids}
        incorrect = {artist_id: set() for artist_id in artist_ids}
        unknown = {}
        unlistened = {}
        total = {}

        for question in questions:
            if question["correct"]:
                correct[track_id2track[question["track_id"]]["artists"][0]].add(question["track_id"])
            else:
                incorrect[track_id2track[question["track_id"]]["artists"][0]].add(question["track_id"])

        for artist_id in artist_ids:
            unknown[artist_id] = correct[artist_id].intersection(incorrect[artist_id])

            track_ids = {track["track_id"] for track in tracks if track["artists"][0] == artist_id}
            unlistened[artist_id] = len(track_ids.difference(correct[artist_id]).difference(incorrect[artist_id]))
            correct[artist_id] = len(correct[artist_id].difference(unknown[artist_id]))
            incorrect[artist_id] = len(incorrect[artist_id].difference(unknown[artist_id]))
            unknown[artist_id] = len(unknown[artist_id])
            total[artist_id] = unknown[artist_id] + correct[artist_id] + incorrect[artist_id] + unlistened[artist_id]

        return cls(
            correct=correct,
            incorrect=incorrect,
            unknown=unknown,
            unlistened=unlistened,
            total=total
        )
