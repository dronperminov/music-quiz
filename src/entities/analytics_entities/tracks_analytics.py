from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from src.enums import Genre


@dataclass
class TracksAnalytics:
    genres: Dict[Genre, int]

    @classmethod
    def evaluate(cls: "TracksAnalytics", tracks: List[dict]) -> "TracksAnalytics":
        genres = defaultdict(int)

        for track in tracks:
            for genre in track["genres"]:
                genres[Genre(genre)] += 1

        total = max(sum(genres.values()), 1)

        return cls(
            genres={genre: count for genre, count in genres.items() if count / total > 0.02}
        )
