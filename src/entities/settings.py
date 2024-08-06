from dataclasses import dataclass
from datetime import datetime

from src.entities.question_settings import QuestionSettings


@dataclass
class Settings:
    username: str
    show_progress: bool
    question_settings: QuestionSettings
    autoplay: bool
    updated_at: datetime

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "show_progress": self.show_progress,
            "question_settings": self.question_settings.to_dict(),
            "autoplay": self.autoplay,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls: "Settings", data: dict) -> "Settings":
        return cls(
            username=data["username"],
            show_progress=data["show_progress"],
            question_settings=QuestionSettings.from_dict(data["question_settings"]),
            autoplay=data["autoplay"],
            updated_at=data["updated_at"]
        )
