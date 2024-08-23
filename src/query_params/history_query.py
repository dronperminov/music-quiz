from dataclasses import dataclass
from typing import List


@dataclass
class HistoryQuery:
    artist_actions: List[str]
    track_actions: List[str]
    limit: int = 100
    skip: int = 0
