import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from src.enums import ArtistType, Genre


@dataclass
class ArtistsSearch:
    query: str
    order: str
    order_type: int
    genres: Dict[Genre, bool]
    artist_type: Dict[ArtistType, bool]
    page: int
    page_size: int

    def to_query(self) -> dict:
        query = {
            "name": {"$regex": re.escape(self.query), "$options": "i"},
            **self.__to_enum_query("genres", self.genres),
            **self.__to_enum_query("artist_type", self.artist_type),
        }

        return query

    def __to_enum_query(self, name: str, values: Dict[Enum, bool]) -> dict:
        if not values:
            return {}

        include_genres = [enum.value for enum, need in values.items() if need]
        exclude_genres = [enum.value for enum, need in values.items() if not need]
        genres = {}

        if include_genres:
            genres["$in"] = include_genres

        if exclude_genres:
            genres["$nin"] = exclude_genres

        return {name: genres}
