from dataclasses import dataclass
from typing import List

from src.entities.analytics_entities.artists_analytics import ArtistsAnalytics
from src.entities.analytics_entities.genres_analytics import TracksAnalytics
from src.entities.analytics_entities.main_analytics import MainAnalytics


@dataclass
class Analytics:
    main: MainAnalytics
    artists: ArtistsAnalytics
    tracks: TracksAnalytics

    @classmethod
    def evaluate(cls: "Analytics", questions: List[dict], tracks: List[dict]) -> "Analytics":
        track_id2artist_ids = {track["track_id"]: track["artists"] for track in tracks}

        return cls(
            main=MainAnalytics.evaluate(questions),
            artists=ArtistsAnalytics.evaluate(questions, track_id2artist_ids),
            tracks=TracksAnalytics.evaluate(tracks)
        )
