from dataclasses import dataclass
from typing import Optional

from fastapi import Query


@dataclass
class NotesSearch:
    query: str = ""
    order: str = "artist_name"
    order_type: int = 1

    page: int = 0
    page_size: int = 20


@dataclass
class NotesSearchQuery:
    query: Optional[str] = Query(None)
    order: Optional[str] = Query(None)
    order_type: Optional[int] = Query(None)

    def is_empty(self) -> bool:
        return self.query is None and self.order is None and self.order_type is None

    def to_params(self) -> Optional[NotesSearch]:
        if self.is_empty():
            return None

        return NotesSearch(
            query=self.query if self.query is not None else "",
            order=self.order if self.order is not None else "artist_name",
            order_type=self.order_type if self.order_type is not None else 1
        )
