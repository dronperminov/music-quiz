from dataclasses import dataclass
from typing import Dict, List, Tuple

from bson import ObjectId

from src.entities.track_modification_settings import TrackModificationSettings
from src.enums import ArtistsCount, Genre, Hits, Language, QuestionType


@dataclass
class QuestionSettings:
    answer_time: float
    genres: Dict[Genre, float]
    years: Dict[Tuple[int, int], float]
    languages: Dict[Language, float]
    artists_count: Dict[ArtistsCount, float]
    listen_count: Tuple[int, int]
    question_types: Dict[QuestionType, float]
    hits: Hits
    black_list: List[ObjectId]
    track_modifications: TrackModificationSettings
    repeat_incorrect_probability: float

    def to_dict(self) -> dict:
        return {
            "answer_time": self.answer_time,
            "genres": {genre.value: value for genre, value in self.genres.items()},
            "years": [{"start_year": start_year, "end_year": end_year, "scale": scale} for (start_year, end_year), scale in self.years.items()],
            "languages": {language.value: value for language, value in self.languages.items()},
            "artists_count": {artists_count.value: value for artists_count, value in self.artists_count.items()},
            "listen_count": self.listen_count,
            "question_types": {question_type.value: value for question_type, value in self.question_types.items()},
            "hits": self.hits.value,
            "black_list": self.black_list,
            "track_modifications": self.track_modifications.to_dict(),
            "repeat_incorrect_probability": self.repeat_incorrect_probability
        }

    @classmethod
    def from_dict(cls: "QuestionSettings", data: dict) -> "QuestionSettings":
        return cls(
            answer_time=data["answer_time"],
            genres={Genre(genre): value for genre, value in data["genres"].items()},
            years={(value["start_year"], value["end_year"]): value["scale"] for value in data["years"]},
            languages={Language(language): value for language, value in data["languages"].items()},
            artists_count={ArtistsCount(artists_count): value for artists_count, value in data["artists_count"].items()},
            listen_count=data["listen_count"],
            question_types={QuestionType(question_type): value for question_type, value in data["question_types"].items()},
            hits=Hits(data["hits"]),
            black_list=data["black_list"],
            track_modifications=TrackModificationSettings.from_dict(data["track_modifications"]),
            repeat_incorrect_probability=data["repeat_incorrect_probability"]
        )
