import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Union

from src.enums import ArtistType, ArtistsCount, Genre, Language
from src.utils.queries import enum_query, interval_query


@dataclass
class ArtistsSearch:
    query: str = ""
    target: str = "all"
    order: str = "listen_count"
    order_type: int = -1
    listen_count: List[Union[str, float, int]] = field(default_factory=lambda: ["", ""])
    years: List[Union[str, float, int]] = field(default_factory=lambda: ["", ""])
    tracks_count: List[Union[str, float, int]] = field(default_factory=lambda: ["", ""])
    added_tracks: List[Union[str, float, int]] = field(default_factory=lambda: ["", ""])
    genres: Dict[Genre, bool] = field(default_factory=dict)
    artist_type: Dict[ArtistType, bool] = field(default_factory=dict)
    artists_count: Dict[ArtistsCount, bool] = field(default_factory=dict)
    language: Dict[Language, bool] = field(default_factory=dict)
    page: int = 0
    page_size: int = 20

    def to_query(self) -> dict:
        query = {
            **self.__to_name_query(),
            **interval_query("listen_count", self.listen_count),
            **interval_query("year", self.years),
            **interval_query("tracks_count", self.tracks_count),
            **interval_query("added_tracks", self.added_tracks),
            **enum_query("genres", self.genres),
            **enum_query("artist_type", self.artist_type),
            **enum_query("artists_count", self.artists_count),
            **enum_query("language", self.language)
        }

        return query

    def replace_enum_query(self, enum_query: dict, enum2sets: Dict[str, set]) -> Tuple[set, set]:
        query_add = set()
        query_remove = set()

        for value in enum_query.get("$in", []):
            query_add.update(enum2sets[value])

        for value in enum_query.get("$nin", []):
            query_remove.update(enum2sets[value])

        return query_add, query_remove

    def __to_name_query(self) -> dict:
        if not self.query:
            return {}

        if re.fullmatch(r"/[^/]+/", self.query):
            return {"name": {"$regex": self.query[1:-1], "$options": "i"}}

        if re.fullmatch(r"\^[^^]+", self.query):
            return {"name": {"$regex": fr"^{re.escape(self.query[1:])}", "$options": "i"}}

        if re.fullmatch(r"[^$]+\$", self.query):
            return {"name": {"$regex": fr"{re.escape(self.query[:-1])}$", "$options": "i"}}

        return {"name": {"$regex": re.escape(self.query), "$options": "i"}}
