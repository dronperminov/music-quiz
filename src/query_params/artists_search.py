import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Union

from src.enums import ArtistType, ArtistsCount, Genre, Language


@dataclass
class ArtistsSearch:
    query: str = ""
    order: str = "listen_count"
    order_type: int = -1
    listen_count: List[Union[str, float]] = field(default_factory=lambda: ["", ""])
    genres: Dict[Genre, bool] = field(default_factory=dict)
    artist_type: Dict[ArtistType, bool] = field(default_factory=dict)
    artists_count: Dict[ArtistsCount, bool] = field(default_factory=dict)
    language: Dict[Language, bool] = field(default_factory=dict)
    page: int = 0
    page_size: int = 20

    def to_query(self) -> dict:
        query = {
            **self.__to_name_query(),
            **self.__to_interval_query("listen_count", self.listen_count),
            **self.__to_enum_query("genres", self.genres),
            **self.__to_enum_query("artist_type", self.artist_type),
            **self.__to_enum_query("artists_count", self.artists_count),
            **self.__to_enum_query("language", self.language)
        }

        return query

    def replace_enum_query(self, enum_query: dict, enum2sets: Dict[str, set]) -> set:
        query = set()

        for value in enum_query.get("$in", []):
            query.update(enum2sets[value])

        for value in enum_query.get("$nin", []):
            query.difference_update(enum2sets[value])

        return query

    def __to_name_query(self) -> dict:
        if not self.query:
            return {}

        return {"name": {"$regex": re.escape(self.query), "$options": "i"}}

    def __to_interval_query(self, name: str, interval: List[Union[str, float]]) -> dict:
        value_from, value_to = interval
        query = {}

        if isinstance(value_from, float):
            query["$gte"] = value_from

        if isinstance(value_to, float):
            query["$lte"] = value_to

        return {name: query} if query else {}

    def __to_enum_query(self, name: str, values: Dict[Enum, bool]) -> dict:
        if not values:
            return {}

        include_values = [enum.value for enum, need in values.items() if need]
        exclude_values = [enum.value for enum, need in values.items() if not need]
        query = {}

        if include_values:
            query["$in"] = include_values

        if exclude_values:
            query["$nin"] = exclude_values

        return {name: query}
