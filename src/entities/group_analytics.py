from dataclasses import dataclass
from typing import List

from src.entities.analytics_entities.group_artists_analytics import GroupArtistsAnalytics
from src.entities.analytics_entities.group_tracks_analytics import GroupTracksAnalytics
from src.entities.analytics_entities.main_analytics import MainAnalytics


@dataclass
class GroupAnalytics:
    main: MainAnalytics
    tracks: GroupTracksAnalytics
    artists: GroupArtistsAnalytics

    @classmethod
    def evaluate(cls: "GroupAnalytics", artist_ids: List[int], questions: List[dict], tracks: List[dict]) -> "GroupAnalytics":
        return cls(
            main=MainAnalytics.evaluate(questions),
            tracks=GroupTracksAnalytics.evaluate(questions, tracks),
            artists=GroupArtistsAnalytics.evaluate(artist_ids, questions, tracks)
        )
