from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Tuple, Union

from src.entities.track_modification_settings import TrackModificationSettings
from src.enums import ArtistsCount, Genre, Hits, Language, QuestionType
from src.utils.queries import interval_query

QUESTION_YEARS = ["", 1980, 1990, 2000, 2010, 2015, 2020, ""]


@dataclass
class QuestionSettings:
    answer_time: float
    genres: Dict[Genre, float]
    years: Dict[Union[Tuple[Union[int, str], Union[int, str]], str], float]
    languages: Dict[Language, float]
    artists_count: Dict[ArtistsCount, float]
    listen_count: Tuple[Union[int, str], Union[int, str]]
    question_types: Dict[QuestionType, float]
    hits: Hits
    black_list: List[int]
    track_modifications: TrackModificationSettings
    repeat_incorrect_probability: float

    def __post_init__(self) -> None:
        self.genres = {genre: value for genre, value in self.genres.items() if value > 0}
        self.years = {self.__fix_years_key(years): value for years, value in self.years.items() if value > 0}
        self.languages = {language: value for language, value in self.languages.items() if value > 0}
        self.artists_count = {artists_count: value for artists_count, value in self.artists_count.items() if value > 0}
        self.question_types = {question_type: value for question_type, value in self.question_types.items() if value > 0}

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

    @classmethod
    def default(cls: "QuestionSettings") -> "QuestionSettings":
        years = cls.year_intervals()

        return cls(
            answer_time=0,
            genres={genre: 1 / len(Genre) for genre in Genre},
            years={(start_year, end_year): 1 / len(years) for start_year, end_year in years},
            languages={language: 1 / (len(Language) - 1) for language in Language},  # exclude unknown
            artists_count={artists_count: 1 / len(ArtistsCount) for artists_count in ArtistsCount},
            listen_count=("", ""),
            question_types={question_type: 1 / len(QuestionType) for question_type in QuestionType},
            hits=Hits.ALL,
            black_list=[],
            track_modifications=TrackModificationSettings(change_playback_rate=False, probability=0),
            repeat_incorrect_probability=0.04
        )

    @staticmethod
    def year_intervals() -> List[Tuple[Union[int, str], Union[int, str]]]:
        years = []

        for i, year in enumerate(QUESTION_YEARS[:-1]):
            years.append((year, QUESTION_YEARS[i + 1] - 1 if QUESTION_YEARS[i + 1] != "" else ""))

        return years

    def to_artist_query(self) -> dict:
        query = interval_query("listen_count", self.listen_count)

        if self.black_list:
            query["artist_id"] = {"$nin": self.black_list}

        return query

    def to_tracks_query(self) -> dict:
        question_type_queries = [question_type.to_query() for question_type in self.question_types]
        years = [self.__replace_years(start_year, end_year) for start_year, end_year in self.years]

        query = {}

        if len(self.genres) < len(Genre):
            query["genres"] = {"$in": [genre.value for genre in self.genres]}

        if len(years) < len(QUESTION_YEARS) - 1:
            query["year"] = {"$in": self.__get_years_list(years)}

        if len(self.languages) < len(Language) - 1:  # ignore UNKNOWN
            query["language"] = {"$in": [language.value for language in self.languages]}

        if len(self.artists_count) < len(ArtistsCount):
            query["artists_count"] = {"$in": [artists_count.value for artists_count in self.artists_count]}

        if {} in question_type_queries:
            return query

        if len(question_type_queries) == 1:
            query = {**query, **question_type_queries[0]}
        else:
            query["$or"] = question_type_queries

        return query

    def __fix_years_key(self, years: Union[Tuple[Union[int, str], Union[int, str]], str]) -> Tuple[Union[int, str], Union[int, str]]:
        if isinstance(years, str):
            start, end = years.split("-")
            start = "" if start == "" else int(start)
            end = "" if end == "" else int(end)
            return start, end

        return years

    def __replace_years(self, start_year: Union[int, str], end_year: Union[int, str]) -> Tuple[int, int]:
        if start_year == "":
            start_year = 1950

        if end_year == "":
            end_year = date.today().year

        return start_year, end_year

    def __get_years_list(self, year_intervals: List[Tuple[int, int]]) -> List[int]:
        years = []

        for start_year, end_year in year_intervals:
            for year in range(start_year, end_year + 1):
                years.append(year)

        return sorted(years)
