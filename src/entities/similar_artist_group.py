from dataclasses import dataclass
from typing import List


@dataclass
class SimilarArtistsGroup:
    creator: str
    group_id: int
    name: str
    description: str
    artist_ids: List[int]
    image_url: str
