import re
from dataclasses import dataclass
from typing import Dict

from src.enums import Genre


@dataclass
class ArtistsSearch:
    query: str
    order: str
    order_type: int
    genres: Dict[Genre, bool]
    page: int
    page_size: int

    def to_query(self) -> dict:
        query = {
            "name": {"$regex": re.escape(self.query), "$options": "i"},
            **self.__to_genres_query()
        }

        return query

    def __to_genres_query(self) -> dict:
        if not self.genres:
            return {}

        include_genres = [genre.value for genre, need in self.genres.items() if need]
        exclude_genres = [genre.value for genre, need in self.genres.items() if not need]
        genres = {}

        if include_genres:
            genres["$in"] = include_genres

        if exclude_genres:
            genres["$nin"] = exclude_genres

        return {"genres": genres}
