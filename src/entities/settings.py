from dataclasses import dataclass
from datetime import datetime

from src.entities.question_settings import QuestionSettings
from src.query_params.main_settings import MainSettings


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

    @classmethod
    def default(cls: "Settings", username: str) -> "Settings":
        return cls(
            username=username,
            show_progress=True,
            question_settings=QuestionSettings.default(),
            autoplay=True,
            updated_at=datetime.now().replace(microsecond=0)
        )

    def update_main(self, main_settings: MainSettings) -> "Settings":
        self.autoplay = main_settings.autoplay
        self.show_progress = main_settings.show_progress
        self.updated_at = datetime.now()
        return self

    def update_question(self, question_settings: QuestionSettings) -> "Settings":
        self.question_settings = question_settings
        self.updated_at = datetime.now()
        return self
