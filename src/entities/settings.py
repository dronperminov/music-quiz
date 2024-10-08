from dataclasses import dataclass
from datetime import datetime

from src.entities.artists_group_settings import ArtistsGroupSettings
from src.entities.question_settings import QuestionSettings
from src.query_params.main_settings import MainSettings


@dataclass
class Settings:
    username: str
    show_progress: bool
    question_settings: QuestionSettings
    artists_group_settings: ArtistsGroupSettings
    autoplay: bool
    updated_at: datetime
    show_knowledge_status: bool

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "show_progress": self.show_progress,
            "question_settings": self.question_settings.to_dict(),
            "artists_group_settings": self.artists_group_settings.to_dict(),
            "autoplay": self.autoplay,
            "show_knowledge_status": self.show_knowledge_status,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls: "Settings", data: dict) -> "Settings":
        return cls(
            username=data["username"],
            show_progress=data["show_progress"],
            question_settings=QuestionSettings.from_dict(data["question_settings"]),
            artists_group_settings=ArtistsGroupSettings.from_dict(data["artists_group_settings"]),
            autoplay=data["autoplay"],
            show_knowledge_status=data["show_knowledge_status"],
            updated_at=data["updated_at"]
        )

    @classmethod
    def default(cls: "Settings", username: str) -> "Settings":
        return cls(
            username=username,
            show_progress=True,
            question_settings=QuestionSettings.default(),
            artists_group_settings=ArtistsGroupSettings.default(),
            autoplay=True,
            show_knowledge_status=True,
            updated_at=datetime.now().replace(microsecond=0)
        )

    def update_main(self, main_settings: MainSettings) -> "Settings":
        self.autoplay = main_settings.autoplay
        self.show_progress = main_settings.show_progress
        self.show_knowledge_status = main_settings.show_knowledge_status
        self.updated_at = datetime.now()
        return self

    def update_question(self, question_settings: QuestionSettings) -> "Settings":
        self.question_settings = question_settings
        self.updated_at = datetime.now()
        return self

    def update_artists_group(self, artists_group_settings: ArtistsGroupSettings) -> "Settings":
        self.artists_group_settings = artists_group_settings
        self.updated_at = datetime.now()
        return self
