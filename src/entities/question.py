import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from typing_extensions import Self

from src.entities.artist import Artist
from src.entities.question_settings import QuestionSettings
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

    def init_base(self, question_type: QuestionType, username: str, settings: QuestionSettings, track_id: int, group_id: Optional[int]) -> None:
        self.question_type = question_type
        self.username = username
        self.group_id = group_id
        self.track_id = track_id

        self.track_modifications = TrackModifications.from_settings(settings.track_modifications)
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
    def from_dict(cls: Self, data: dict) -> Self:
        question_type = QuestionType(data["question_type"])

        if question_type == QuestionType.ARTIST_BY_TRACK:
            question = ArtistByTrackQuestion(data["title"], data["answer"], data["question_seek"])
        elif question_type == QuestionType.ARTIST_BY_INTRO:
            question = ArtistByIntroQuestion(data["title"], data["answer"], data["question_seek"], data["question_timecode"])
        elif question_type == QuestionType.NAME_BY_TRACK:
            question = NameByTrackQuestion(data["title"], data["answer"], data["question_seek"])
        elif question_type == QuestionType.LINE_BY_TEXT:
            question = LineByTextQuestion(data["title"], data["answer"], data["question_seek"], data["lines"], data["question_timecode"], data["answer_seek"])
        elif question_type == QuestionType.LINE_BY_CHORUS:
            question = LineByChorusQuestion(data["title"], data["answer"], data["question_seek"], data["lines"], data["question_timecode"], data["answer_seek"])
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

    def is_valid(self, track_ids: Dict[int, dict], settings: QuestionSettings) -> bool:
        return self.track_id in track_ids and self.question_type in settings.question_types

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings) -> Self:
        self.track_modifications = TrackModifications.from_settings(settings.track_modifications)
        return self

    @staticmethod
    def get_artist_types(track: Track, artist_id2artist: Dict[int, Artist], simple: bool) -> str:
        if len(track.artists) == 2 and artist_id2artist[track.artists[0]].artist_type == artist_id2artist[track.artists[1]].artist_type:
            return artist_id2artist[track.artists[0]].artist_type.to_pair_title(simple=simple)

        artist_types = [artist_id2artist[artist_id].artist_type.to_title(simple=simple) for artist_id in track.artists]

        if len(artist_types) == 1:
            return artist_types[0]

        return f'{", ".join(artist_types[:-1])} и {artist_types[-1]}'

    @staticmethod
    def get_random_seek(track: Track, start_from_chorus: bool) -> float:
        if track.lyrics and track.lyrics.lrc:
            if start_from_chorus and track.lyrics.chorus:
                start, end = track.lyrics.chorus[0] if len(track.lyrics.chorus) == 1 else random.choice(track.lyrics.chorus[:-1])
                return track.lyrics.lines[start].time

            line = random.choice(track.lyrics.lines[:len(track.lyrics) * 3 // 4])
            return line.time

        if track.duration > 0:
            return round(random.random() * track.duration * 0.75, 2)

        return 0


@dataclass
class ArtistByTrackQuestion(Question):
    @classmethod
    def generate(cls: Self, track: Track, artist_id2artist: Dict[int, Artist], username: str, settings: QuestionSettings, group_id: Optional[int]) -> Self:
        question = cls(
            title=ArtistByTrackQuestion.get_title(track, artist_id2artist, settings, group_id),
            answer=", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists),
            question_seek=Question.get_random_seek(track, settings.start_from_chorus),
        )

        question.init_base(question_type=QuestionType.ARTIST_BY_TRACK, username=username, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings) -> Self:
        super().update(track, artist_id2artist, settings)
        self.title = ArtistByTrackQuestion.get_title(track, artist_id2artist, settings, self.group_id)
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)
        return self

    @staticmethod
    def get_title(track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings, group_id: Optional[int]) -> str:
        if group_id:
            return f'Назовите автор{"а" if len(track.artists) == 1 else "ов"}'

        return f"Назовите {Question.get_artist_types(track, artist_id2artist, settings.show_simple_artist_type)}"


@dataclass
class NameByTrackQuestion(Question):
    @classmethod
    def generate(cls: Self, track: Track, username: str, settings: QuestionSettings, group_id: Optional[int]) -> Self:
        question = cls(
            title="Назовите название трека",
            answer=track.title,
            question_seek=Question.get_random_seek(track, settings.start_from_chorus)
        )

        question.init_base(question_type=QuestionType.NAME_BY_TRACK, username=username, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings) -> Self:
        super().update(track, artist_id2artist, settings)
        self.title = "Назовите название трека"
        self.answer = track.title
        return self


@dataclass
class ArtistByIntroQuestion(Question):
    question_timecode: str

    @classmethod
    def generate(cls: Self, track: Track, artist_id2artist: Dict[int, Artist], username: str, settings: QuestionSettings, group_id: Optional[int]) -> Self:
        question = cls(
            title=ArtistByTrackQuestion.get_title(track, artist_id2artist, settings, group_id),
            answer=", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists),
            question_seek=0,
            question_timecode=f"0,{round(track.lyrics.lines[0].time - 1, 2)}"
        )

        question.init_base(question_type=QuestionType.ARTIST_BY_INTRO, username=username, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "question_timecode": self.question_timecode
        }

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings) -> Self:
        super().update(track, artist_id2artist, settings)
        self.title = self.get_title(track, artist_id2artist, settings, self.group_id)
        self.answer = ", ".join(f'<a class="link" href="/artists/{artist_id}">{artist_id2artist[artist_id].name}</a>' for artist_id in track.artists)
        return self

    @staticmethod
    def get_title(track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings, group_id: Optional[int]) -> str:
        if group_id:
            return f'Назовите автор{"а" if len(track.artists) == 1 else "ов"} по вступлению'

        return f"Назовите {Question.get_artist_types(track, artist_id2artist, settings.show_simple_artist_type)} по вступлению"


@dataclass
class LineByTextQuestion(Question):
    lines: List[str]
    question_timecode: str
    answer_seek: float

    @classmethod
    def generate(cls: Self, track: Track, username: str, settings: QuestionSettings, group_id: Optional[int]) -> Self:
        start_index = random.randint(0, len(track.lyrics.lines) - 4)
        start_time = track.lyrics.lines[start_index].time - 0.1
        end_time = track.lyrics.lines[start_index + 3].time

        question = cls(
            title="Напишите следующую строку песни",
            answer=track.lyrics.lines[start_index + 3].text,
            question_seek=start_time,
            lines=[track.lyrics.lines[start_index + i].text for i in range(3)],
            answer_seek=end_time,
            question_timecode=f"{start_time},{end_time - 0.1}"
        )

        question.init_base(question_type=QuestionType.LINE_BY_TEXT, username=username, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings) -> Self:
        super().update(track, artist_id2artist, settings)
        return self

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "lines": self.lines,
            "answer_seek": self.answer_seek,
            "question_timecode": self.question_timecode
        }


@dataclass
class LineByChorusQuestion(Question):
    lines: List[str]
    question_timecode: str
    answer_seek: float

    @classmethod
    def generate(cls: Self, track: Track, username: str, settings: QuestionSettings, group_id: Optional[int]) -> Self:
        start_index, end_index = random.choice(track.lyrics.chorus[:-1])

        if end_index - start_index > 3:
            start_index = random.randint(start_index, end_index - 3)
            end_index = min(start_index + random.randint(3, 5), end_index)

        start_time = track.lyrics.lines[start_index].time - 0.1
        end_time = track.lyrics.lines[end_index].time

        question = cls(
            title="Напишите следующую строку припева",
            answer=track.lyrics.lines[end_index].text,
            question_seek=start_time,
            lines=[track.lyrics.lines[i].text for i in range(start_index, end_index)],
            answer_seek=end_time,
            question_timecode=f"{start_time},{end_time - 0.1}"
        )

        question.init_base(question_type=QuestionType.LINE_BY_CHORUS, username=username, settings=settings, track_id=track.track_id, group_id=group_id)
        return question

    def update(self, track: Track, artist_id2artist: Dict[int, Artist], settings: QuestionSettings) -> Self:
        super().update(track, artist_id2artist, settings)
        return self

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "lines": self.lines,
            "answer_seek": self.answer_seek,
            "question_timecode": self.question_timecode
        }
