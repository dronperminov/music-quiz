from dataclasses import dataclass


@dataclass
class ArtistsGroupsSearch:
    order: str = "group_id"
    page: int = 0
    page_size: int = 20
