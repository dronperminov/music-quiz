from dataclasses import dataclass
from typing import Dict, List

from src.entities.analytics_entities.artists_analytics import ArtistsAnalytics
from src.entities.analytics_entities.main_analytics import MainAnalytics


@dataclass
class Analytics:
    main: MainAnalytics
    artists: ArtistsAnalytics

    @classmethod
    def evaluate(cls: "Analytics", questions: List[dict], track_id2artist_ids: Dict[int, List[int]]) -> "Analytics":
        return cls(
            main=MainAnalytics.evaluate(questions),
            artists=ArtistsAnalytics.create(questions, track_id2artist_ids)
        )
