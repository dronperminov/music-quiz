from enum import Enum


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
