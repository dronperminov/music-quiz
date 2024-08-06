from dataclasses import dataclass
from datetime import datetime


@dataclass
class Metadata:
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime

    def to_dict(self) -> dict:
        return {
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_by": self.updated_by,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls: "Metadata", data: dict) -> "Metadata":
        return cls(
            created_by=data["created_by"],
            created_at=data["created_at"],
            updated_by=data["updated_by"],
            updated_at=data["updated_at"]
        )
