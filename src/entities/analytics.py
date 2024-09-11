from dataclasses import dataclass
from typing import List

from src.entities.analytics_entities.artists_analytics import ArtistsAnalytics
from src.entities.analytics_entities.main_analytics import MainAnalytics
from src.entities.analytics_entities.period_analytics import PeriodAnalytics
from src.entities.analytics_entities.tracks_analytics import TracksAnalytics


@dataclass
class Analytics:
    main: MainAnalytics
    artists: ArtistsAnalytics
    tracks: TracksAnalytics
    period: PeriodAnalytics

    @classmethod
    def evaluate(cls: "Analytics", questions: List[dict], tracks: List[dict]) -> "Analytics":
        track_id2artist_ids = {track["track_id"]: track["artists"] for track in tracks}
        correct_track_ids = [question["track_id"] for question in questions if question["correct"]]
        incorrect_track_ids = [question["track_id"] for question in questions if not question["correct"]]

        return cls(
            main=MainAnalytics.evaluate(questions),
            artists=ArtistsAnalytics.evaluate(questions, track_id2artist_ids),
            tracks=TracksAnalytics.evaluate(tracks, correct=correct_track_ids, incorrect=incorrect_track_ids),
            period=PeriodAnalytics.evaluate(questions)
        )
