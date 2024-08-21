import json
from dataclasses import dataclass
from typing import Optional

from fastapi import Query

from src.query_params.artists_search import ArtistsSearch


@dataclass
class ArtistsSearchQuery:
    query: Optional[str] = Query(None)
    target: Optional[str] = Query(None)
    order: Optional[str] = Query(None)
    order_type: Optional[int] = Query(None)
    listen_count: Optional[str] = Query(None)
    tracks_count: Optional[str] = Query(None)
    added_tracks: Optional[str] = Query(None)
    genres: Optional[str] = Query(None)
    artist_type: Optional[str] = Query(None)
    artists_count: Optional[str] = Query(None)
    language: Optional[str] = Query(None)

    def is_empty(self) -> bool:
        feilds = [
            self.query, self.target, self.order, self.order_type, self.listen_count, self.tracks_count, self.added_tracks, self.genres, self.artist_type, self.artists_count,
            self.language
        ]

        for field in feilds:
            if field is not None:
                return False

        return True

    def to_search_params(self, with_user: bool) -> Optional[ArtistsSearch]:
        if self.is_empty():
            return None

        return ArtistsSearch(
            query=self.query if self.query is not None else "",
            target=self.target if self.target is not None and with_user else "all",
            order=self.order if self.order is not None else "listen_count",
            order_type=self.order_type if self.order_type is not None else -1,
            listen_count=json.loads(self.listen_count) if self.listen_count is not None else ["", ""],
            tracks_count=json.loads(self.tracks_count) if self.tracks_count is not None else ["", ""],
            added_tracks=json.loads(self.added_tracks) if self.added_tracks is not None else ["", ""],
            genres=json.loads(self.genres) if self.genres is not None else {},
            artist_type=json.loads(self.artist_type) if self.artist_type is not None else {},
            artists_count=json.loads(self.artists_count) if self.artists_count is not None else {},
            language=json.loads(self.language) if self.language is not None else {}
        )
