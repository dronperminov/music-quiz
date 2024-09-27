from dataclasses import dataclass

from fastapi import Query


@dataclass
class MarkupTrack:
    track_id: int = Query(0)
    language: str = Query("")
    artist_id: int = Query(0)
    min_chorus: int = Query(0)
    max_chorus: int = Query(100)

    def to_params(self) -> str:
        return "&".join([
            f"track_id={self.track_id}",
            f"language={self.language}",
            f"min_chorus={self.min_chorus}",
            f"max_chorus={self.max_chorus}",
        ])

    def to_query(self) -> dict:
        if self.track_id:
            return {"track_id": self.track_id}

        query = {"lyrics": {"$ne": None}, "lyrics.lrc": True, "lyrics.validated": False}

        if self.language != "":
            query["language"] = self.language

        if self.artist_id > 0:
            query["artists"] = [self.artist_id]

        if self.min_chorus > 0:
            query[f"lyrics.chorus.{self.min_chorus - 1}"] = {"$exists": True}

        if self.max_chorus > 0:
            query[f"lyrics.chorus.{self.max_chorus}"] = {"$exists": False}

        return query
