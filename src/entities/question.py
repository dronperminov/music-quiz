import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Set

from src.entities.artist import Artist
from src.entities.settings import Settings
from src.entities.track import Track
from src.entities.track_modifications import TrackModifications
from src.enums import QuestionType
from src.query_params.question_answer import QuestionAnswer


@dataclass
class Question:
    username: str = field(init=False)
    question_type: QuestionType = field(init=False)
    group_id: Optional[int] = field(init=False)
    track_id: int = field(init=False)
    title: str
    answer: str
    question_seek: float
    track_modifications: TrackModifications = field(init=False)
    correct: Optional[bool] = field(init=False)
    answer_time: Optional[float] = field(init=False)
    timestamp: datetime = field(init=False)

    def init_base(self, question_type: QuestionType, settings: Settings, track_id: int, group_id: Optional[int]) -> None:
        self.question_type = question_type
        self.username = settings.username
        self.group_id = group_id
        self.track_id = track_id

        self.track_modifications = TrackModifications.from_settings(settings.question_settings.track_modifications)
        self.remove_answer()

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "question_type": self.question_type.value,
            "group_id": self.group_id,
            "track_id": self.track_id,
            "title": self.title,
            "answer": self.answer,
            "question_seek": self.question_seek,
            "track_modifications": self.track_modifications.to_dict(),
            "correct": self.correct,
            "answer_time": self.answer_time,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls: "Question", data: dict) -> "Question":
        question_type = QuestionType(data["question_type"])

        if question_type == QuestionType.ARTIST_BY_TRACK:
            question = ArtistByTrackQuestion(data["title"], data["answer"], data["question_seek"])
        elif question_type == QuestionType.ARTIST_BY_INTRO:
            question = ArtistByIntroQuestion(data["title"], data["answer"], data["question_seek"], data["question_timecode"])
        elif question_type == QuestionType.NAME_BY_TRACK:
            question = NameByTrackQuestion(data["title"], data["answer"], data["question_seek"])
        else:
            raise ValueError(f'Invalid question_type "{question_type}"')

        question.question_type = question_type
        question.username = data["username"]
        question.group_id = data["group_id"]
        question.track_id = data["track_id"]
        question.track_modifications = TrackModifications.from_dict(data["track_modifications"])
        question.correct = data["correct"]
        question.answer_time = data["answer_time"]
        question.timestamp = data["timestamp"]

        return question

    def set_answer(self, answer: QuestionAnswer) -> None:
        self.correct = answer.correct
        self.answer_time = answer.answer_time
        self.timestamp = datetime.now()

    def remove_answer(self) -> None:
        self.correct = None
        self.answer_time = None
        self.timestamp = datetime.now()

    def is_valid(self, track_ids: Set[int], settings: Settings) -> bool:
        return self.track_id in track_ids and self.question_type in settings.question_settings.question_types

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings) -> "Question":
        self.track_modifications = TrackModifications.from_settings(settings.question_settings.track_modifications)
        return self

    @staticmethod
    def get_artist_types(track: Track, artist_id2artist: Dict[int, Artist], simple: bool) -> str:
        artist_types = [artist_id2artist[artist_id].artist_type.to_title(simple=simple) for artist_id in track.artists]

        if len(artist_types) == 1:
            return artist_types[0]

        return f'{", ".join(artist_types[:-1])} и {artist_types[-1]}'

    @staticmethod
    def get_random_seek(track: Track, start_from_chorus: bool) -> float:
        if track.lyrics and track.lyrics.lrc:
            if start_from_chorus and track.lyrics.chorus:
                start, end = random.choice(track.lyrics.chorus)
                return track.lyrics.lines[start].time

            line = random.choice(track.lyrics.lines[:len(track.lyrics) * 3 // 4])
            return line.time

        if track.duration > 0:
            return round(random.random() * track.duration * 0.75, 2)

        return 0


@dataclass
class ArtistByTrackQuestion(Question):
    @classmethod
    def generate(cls: "ArtistByTrackQuestion", track: Track, artist_id2artist: Dict[int, Artist], settings: Settings, group_id: Optional[int]) -> "ArtistByTrackQuestion":
        question = cls(
            title=f"Назовите {Question.get_artist_types(track, artist_id2artist, settings.question_settings.show_simple_artist_type)}",
            answer=", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists),
            question_seek=Question.get_random_seek(track, settings.question_settings.start_from_chorus),
        )

        question.init_base(question_type=QuestionType.ARTIST_BY_TRACK, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings) -> "ArtistByTrackQuestion":
        super().update(track, artist_id2artist, settings)
        self.title = f"Назовите {Question.get_artist_types(track, artist_id2artist, settings.question_settings.show_simple_artist_type)}"
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)
        return self


@dataclass
class NameByTrackQuestion(Question):
    @classmethod
    def generate(cls: "NameByTrackQuestion", track: Track, settings: Settings, group_id: Optional[int]) -> "NameByTrackQuestion":
        question = cls(
            title="Назовите название трека",
            answer=track.title,
            question_seek=Question.get_random_seek(track, settings.question_settings.start_from_chorus)
        )

        question.init_base(question_type=QuestionType.NAME_BY_TRACK, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings) -> "NameByTrackQuestion":
        super().update(track, artist_id2artist, settings)
        self.title = "Назовите название трека"
        self.answer = track.title
        return self


@dataclass
class ArtistByIntroQuestion(Question):
    question_timecode: str

    @classmethod
    def generate(cls: "ArtistByIntroQuestion", track: Track, artist_id2artist: Dict[int, Artist], settings: Settings, group_id: Optional[int]) -> "ArtistByIntroQuestion":
        question = cls(
            title=f"Назовите {Question.get_artist_types(track, artist_id2artist, settings.question_settings.show_simple_artist_type)} по вступлению",
            answer=", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists),
            question_seek=0,
            question_timecode=f"0,{round(track.lyrics.lines[0].time - 1, 2)}"
        )

        question.init_base(question_type=QuestionType.ARTIST_BY_INTRO, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "question_timecode": self.question_timecode
        }

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: Settings) -> "ArtistByIntroQuestion":
        super().update(track, artist_id2artist, settings)
        self.title = f"Назовите {Question.get_artist_types(track, artist_id2artist, settings.question_settings.show_simple_artist_type)} по вступлению"
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)
        return self
