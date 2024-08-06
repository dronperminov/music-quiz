from dataclasses import dataclass
from typing import List

from bson import ObjectId


@dataclass
class SimilarArtistsGroup:
    creator: str
    group_id: ObjectId
    name: str
    description: str
    artist_ids: List[ObjectId]
    image_url: str
