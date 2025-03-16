from enum import Enum


class RepeatStrategy(Enum):
    RECENT_MISTAKES = "recent_mistakes"
    OLD_MISTAKES = "old_mistakes"
    WEIGHTED_ARTISTS = "weighted_artists"
    INTERVAL_TRACKS = "interval_tracks"
