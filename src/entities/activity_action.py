from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ActivityAction:
    username: str
    timestamp: datetime
    group_id: Optional[int]
