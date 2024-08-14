from dataclasses import dataclass


@dataclass
class ArtistsSearch:
    order: str
    order_type: int
    page: int
    page_size: int
