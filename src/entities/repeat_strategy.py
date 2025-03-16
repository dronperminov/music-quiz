import abc
import random
from collections import defaultdict
from typing import Dict, List

from src.entities.question import Question


class RepeatStrategy:
    @abc.abstractmethod
    def get_question(self, questions: List[Question], incorrect_questions: List[Question], track_id2track: Dict[int, dict]) -> Question:
        pass


class RecentMistakesRepeatStrategy(RepeatStrategy):
    def __init__(self, alpha: float = 0.999) -> None:
        self.alpha = alpha

    def get_question(self, questions: List[Question], incorrect_questions: List[Question], track_id2track: Dict[int, dict]) -> Question:
        question_weights = [1 - self.alpha ** (i + 1) for i in range(len(incorrect_questions))]
        return random.choices(incorrect_questions, weights=question_weights, k=1)[0]


class OldMistakesRepeatStrategy(RepeatStrategy):
    def __init__(self, alpha: float = 0.999) -> None:
        self.alpha = alpha

    def get_question(self, questions: List[Question], incorrect_questions: List[Question], track_id2track: Dict[int, dict]) -> Question:
        question_weights = [self.alpha ** (i + 1) for i in range(len(incorrect_questions))]
        return random.choices(incorrect_questions, weights=question_weights, k=1)[0]


class WeightedArtistsRepeatStrategy(RepeatStrategy):
    def get_question(self, questions: List[Question], incorrect_questions: List[Question], track_id2track: Dict[int, dict]) -> Question:
        artists_weights = self.get_artists_weights(questions=questions, track_id2track=track_id2track)
        tracks_weights = self.get_tracks_weights(questions=questions)

        question_weights = []

        for question in incorrect_questions:
            artists_weight = max(artists_weights[artist_id] for artist_id in track_id2track[question.track_id]["artists"])
            track_weight = tracks_weights[question.track_id]
            question_weights.append(artists_weight * track_weight)

        return random.choices(incorrect_questions, weights=question_weights, k=1)[0]

    def get_artists_weights(self, questions: List[Question], track_id2track: Dict[int, dict]) -> Dict[int, float]:
        incorrect = defaultdict(int)
        total = defaultdict(int)

        for question in questions:
            track = track_id2track[question.track_id]

            for artist_id in track["artists"]:
                if not question.correct:
                    incorrect[artist_id] += 1

                total[artist_id] += 1

        return {artist_id: incorrect[artist_id] / total[artist_id] for artist_id in incorrect}

    def get_tracks_weights(self, questions: List[Question]) -> Dict[int, float]:
        incorrect = defaultdict(int)
        total = defaultdict(int)

        for question in questions:
            if not question.correct:
                incorrect[question.track_id] += 1

            total[question.track_id] += 1

        return {track_id: incorrect[track_id] / total[track_id] for track_id in incorrect}


class IntervalsRepeatStrategy(RepeatStrategy):
    def get_question(self, questions: List[Question], incorrect_questions: List[Question], track_id2track: Dict[int, dict]) -> Question:
        tracks_weights = {track_id: 1 for track_id in track_id2track}

        for question in questions:
            if question.correct:
                tracks_weights[question.track_id] /= 2
            else:
                tracks_weights[question.track_id] = 1

        question_weights = [tracks_weights[question.track_id] for question in questions]
        return random.choices(questions, weights=question_weights, k=1)[0]
