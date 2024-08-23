from dataclasses import dataclass


@dataclass
class ArtistsGroupsSearch:
    page: int = 0
    page_size: int = 20
