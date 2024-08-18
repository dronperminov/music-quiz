from enum import Enum
from typing import List


class Hits(Enum):
    ONLY_HITS = "only-hits"
    WITHOUT_HITS = "without-hits"
    ALL = "all"

    def to_rus(self) -> str:
        hits2rus = {
            Hits.ONLY_HITS: "только хиты",
            Hits.WITHOUT_HITS: "без хитов",
            Hits.ALL: "все подряд",
        }

        return hits2rus[self]

    def filter_tracks(self, track_positions: List[dict]) -> List[int]:
        return [track_position["track_id"] for track_position in track_positions if self.__check_position(track_position["position"])]

    def __check_position(self, position: int) -> bool:
        if self == Hits.ONLY_HITS:
            return position <= 5

        if self == Hits.WITHOUT_HITS:
            return position > 5

        return True
