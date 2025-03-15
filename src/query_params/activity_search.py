from dataclasses import dataclass


@dataclass
class ActivitySearch:
    page: int = 0
    page_size: int = 10
