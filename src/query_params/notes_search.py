import re
from dataclasses import dataclass
from typing import Optional

from fastapi import Query


@dataclass
class NotesSearch:
    query: str = ""
    order: str = "artist_name"
    order_type: int = 1
    with_text: str = "any"

    page: int = 0
    page_size: int = 20

    def to_query(self) -> dict:
        query = {**self.to_text_query()}

        if not self.query:
            if self.with_text == "text":
                query["text"] = {"$ne": ""}
            elif self.with_text == "no-text":
                query["text"] = ""

        return query

    def to_text_query(self) -> dict:
        return {"text": {"$regex": re.escape(self.query), "$options": "i"}} if self.query else {}


@dataclass
class NotesSearchQuery:
    query: Optional[str] = Query(None)
    order: Optional[str] = Query(None)
    order_type: Optional[int] = Query(None)
    with_text: Optional[str] = Query(None)

    def is_empty(self) -> bool:
        return self.query is None and self.order is None and self.order_type is None and self.with_text is None

    def to_params(self) -> Optional[NotesSearch]:
        if self.is_empty():
            return None

        return NotesSearch(
            query=self.query if self.query is not None else "",
            order=self.order if self.order is not None else "artist_name",
            order_type=self.order_type if self.order_type is not None else 1,
            with_text=self.with_text if self.with_text is not None else "any"
        )
