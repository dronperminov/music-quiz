from dataclasses import dataclass
from typing import List, Tuple, Union

from src.entities.question_settings import QuestionSettings
from src.entities.track_modification_settings import TrackModificationSettings
from src.enums import ArtistsCount, Genre, Language, QuestionType, QuizTourType


@dataclass
class QuizTourAdd:
    name: str
    description: str
    questions_count: int
    years: str
    genres: str
    language: str
    positions: str
    mechanics: QuizTourType
    image_dir: str
    listen_count: Tuple[Union[int, str], Union[int, str]]

    def to_settings(self) -> QuestionSettings:
        years = {
            "all": {(1980, 1989): 1, (1990, 1999): 1, (2000, 2009): 1, (2010, 2014): 1, (2015, 2019): 1, (2020, ""): 1},
            "1990": {(1990, 1999): 1},
            "1990-2000": {(1990, 1999): 1, (2000, 2009): 1},
            "2000": {(2000, 2009): 1},
            "2000-2010": {(2000, 2009): 0.5, (2010, 2019): 0.5},
            "modern": {(2010, 2014): 1, (2015, 2019): 2, (2020, ""): 4},
            "2020": {(2020, ""): 1},
            "xx century": {(1980, 1989): 1, (1990, 1999): 1},
            "xxi century": {(2000, 2009): 1, (2010, 2014): 1, (2015, 2019): 1, (2020, ""): 1}
        }[self.years]

        genres = {
            "all": {genre: 1 / len(Genre) for genre in Genre},
            "rock": {Genre.ROCK: 1},
            "hip-hop": {Genre.HIP_HOP: 1},
            "pop": {Genre.POP: 1},
        }[self.genres]

        languages = {
            "all": {Language.RUSSIAN: 0.5, Language.FOREIGN: 0.5},
            "russian": {Language.RUSSIAN: 1},
            "foreign": {Language.FOREIGN: 1},
        }[self.language]

        track_position = {
            "all": ("", ""),
            "top1": ("", 1),
            "top3": ("", 3),
            "hits": ("", 5),
            "normal": ("", 10),
            "unhackneyed": (11, "")
        }[self.positions]

        return QuestionSettings(
            answer_time=0,
            show_simple_artist_type=False,
            start_from_chorus=self.positions == "hits",
            genres=genres,
            years=years,
            languages=languages,
            artists_count={ArtistsCount.SOLO: 1},
            listen_count=self.listen_count,
            question_types={QuestionType.ARTIST_BY_TRACK: 1},
            track_position=track_position,
            black_list=[],
            repeat_incorrect_probability=0,
            track_modifications=TrackModificationSettings(change_playback_rate=False, probability=0)
        )

    def to_tags(self) -> List[str]:
        tags = []

        if self.language in ["all", "russian"]:
            tags.append("russian")

        if self.language in ["all", "foreign"]:
            tags.append("foreign")

        if self.genres != "all":
            tags.append(self.genres)

        if self.positions in ["hits", "unhackneyed"]:
            tags.append(self.positions)

        if self.positions in ["top1", "top3"]:
            tags.append("hits")

        if self.years != "all":
            tags.extend(self.years.split("-") if "-" in self.years else [self.years])

        return tags
