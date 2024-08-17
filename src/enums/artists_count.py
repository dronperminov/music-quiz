from enum import Enum


class ArtistsCount(Enum):
    SOLO = "solo"
    FEAT = "feat"

    def to_rus(self) -> str:
        artists_count2rus = {
            ArtistsCount.SOLO: "сольные",
            ArtistsCount.FEAT: "фиты"
        }

        return artists_count2rus[self]
