from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from src.entities.question_settings import QuestionSettings
from src.enums import Genre


@dataclass
class TracksAnalytics:
    genres: Dict[Genre, int]
    years_correct: Dict[str, int]
    years_incorrect: Dict[str, int]
    years_total: Dict[str, int]

    @classmethod
    def evaluate(cls: "TracksAnalytics", tracks: List[dict], correct: List[int], incorrect: List[int]) -> "TracksAnalytics":
        intervals = QuestionSettings.year_intervals()
        years_keys = [f"{intervals[0][1]}", *[f"{start_year}-{end_year}" for start_year, end_year in intervals[1:-1]], f"{intervals[-1][0]}"]
        track_id2year_key = {track["track_id"]: TracksAnalytics.year2label(track["year"], intervals=intervals) for track in tracks}

        genres = defaultdict(int)
        years_correct = {key: 0 for key in years_keys}
        years_incorrect = {key: 0 for key in years_keys}
        years_total = {key: 0 for key in years_keys}

        for track in tracks:
            for genre in track["genres"]:
                genres[Genre(genre)] += 1

        for track_id in correct:
            years_correct[track_id2year_key[track_id]] += 1
            years_total[track_id2year_key[track_id]] += 1

        for track_id in incorrect:
            years_incorrect[track_id2year_key[track_id]] += 1
            years_total[track_id2year_key[track_id]] += 1

        genres_total = max(sum(genres.values()), 1)

        return cls(
            genres={genre: count for genre, count in genres.items() if count / genres_total > 0.02},
            years_correct=years_correct,
            years_incorrect=years_incorrect,
            years_total=years_total
        )

    @staticmethod
    def year2label(track_year: int, intervals: list) -> str:
        if track_year < intervals[0][1]:
            return f"{intervals[0][1]}"

        for start_year, end_year in intervals[1:-1]:
            if start_year <= track_year <= end_year:
                return f"{start_year}-{end_year}"

        return f"{intervals[-1][0]}"
