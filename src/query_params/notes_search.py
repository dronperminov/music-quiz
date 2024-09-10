import re
from dataclasses import dataclass


@dataclass
class NotesSearch:
    query: str = ""
    order: str = "artist_id"
    with_text: str = "any"

    page: int = 0
    page_size: int = 20

    def to_query(self) -> dict:
        query = {**self.to_text_query()}

        if self.with_text == "text":
            query["text"] = {"$ne": ""}
        elif self.with_text == "no-text":
            query["text"] = ""

        return query

    def to_text_query(self) -> dict:
        return {"text": {"$regex": re.escape(self.query), "$options": "i"}} if self.query else {}
