import random
from datetime import datetime
from unittest import TestCase

from bson import ObjectId

from src.entities.artist import Artist
from src.entities.lyrics import Lyrics, LyricsLine
from src.entities.metadata import Metadata
from src.entities.note import Note
from src.entities.question import Question
from src.entities.question_settings import QuestionSettings
from src.entities.settings import Settings
from src.entities.source import HandSource, Source, YandexSource
from src.entities.track import Track
from src.entities.track_landmark import TrackLandmark
from src.entities.track_modification_settings import TrackModificationSettings
from src.entities.track_modifications import TrackModifications
from src.entities.user import User
from src.enums import ArtistType, ArtistsCount, Genre, Hits, Language, QuestionType, UserRole


class AbstractUnitTest(TestCase):
    GENRES = [Genre.ROCK, Genre.POP, Genre.HIP_HOP, Genre.ELECTRO, Genre.DISCO, Genre.JAZZ_SOUL]
    LANGUAGES = [Language.RUSSIAN, Language.FOREIGN]
    ARTISTS_COUNT = [ArtistsCount.SOLO, ArtistsCount.FEAT]
    ARTIST_TYPES = [
        ArtistType.SINGER_MALE, ArtistType.SINGER_FEMALE, ArtistType.PERFORMER_MALE, ArtistType.PERFORMER_FEMALE,
        ArtistType.BAND, ArtistType.PROJECT, ArtistType.DUET, ArtistType.TRIO, ArtistType.DJ, ArtistType.VIA
    ]
    QUESTION_TYPES = [
        QuestionType.ARTIST_BY_TRACK, QuestionType.ARTIST_BY_INTRO, QuestionType.LINE_BY_TEXT,
        QuestionType.LINE_BY_CHORUS, QuestionType.FIRST_WORD_BY_TEXT, QuestionType.LAST_WORD_BY_TEXT,
        QuestionType.FIRST_WORD_BY_CHORUS, QuestionType.LAST_WORD_BY_CHORUS, QuestionType.NAME_BY_TRACK
    ]
    YEARS = [
        (1900, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2024)
    ]
    HITS = [Hits.ONLY_HITS, Hits.WITHOUT_HITS, Hits.ALL]
    USER_ROLES = [UserRole.USER, UserRole.ADMIN, UserRole.OWNER]

    def generate_username(self) -> str:
        return random.choice(["user", "cat", "dog", "admin", "looooooooooooooooong_username"])

    def generate_datetime(self) -> datetime:
        year = random.randint(2020, 2024)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def generate_source(self) -> Source:
        if random.random() < 0.5:
            return YandexSource(yandex_id=str(random.randint(1, 1000)))

        return HandSource()

    def generate_list(self, values: list) -> list:
        return random.sample(values, random.randint(1, len(values)))

    def generate_balance(self, values: list) -> dict:
        return {value: random.randint(1, 10) / 10 for value in values}

    def generate_user(self) -> User:
        return User(
            username=self.generate_username(),
            password_hash="password hash",
            full_name="user full name",
            role=random.choice(self.USER_ROLES),
            avatar_url="url to avatar"
        )

    def generate_lyrics(self) -> Lyrics:
        lines_count = random.randint(20, 20)
        chorus_count = random.randint(0, 3)

        lines = [LyricsLine(time=random.randint(10, 360) / 2, text=f"line{i + 1}") for i in range(lines_count)]
        chorus = []

        for _ in range(chorus_count):
            start = random.randint(0, len(lines) - 4)
            end = start + random.randint(4, 8)
            chorus.append((start, end))

        return Lyrics(lines=lines, chorus=chorus)

    def generate_metadata(self) -> Metadata:
        return Metadata(
            created_by=self.generate_username(),
            created_at=self.generate_datetime(),
            updated_at=datetime.now(),
            updated_by=self.generate_username()
        )

    def generate_track(self, with_lyrics: bool = True) -> Track:
        source = self.generate_source()
        lyrics = self.generate_lyrics() if with_lyrics else None
        genres = self.generate_list(self.GENRES)
        language = random.choice(self.LANGUAGES)
        metadata = self.generate_metadata()

        return Track(
            track_id=ObjectId(),
            source=source,
            title="title",
            artists=[ObjectId() for _ in range(random.randint(1, 5))],
            year=random.randint(2020, 2024),
            lyrics=lyrics,
            genres=genres,
            language=language,
            duration=random.randint(10, 360) / 2,
            downloaded=random.random() < 0.5,
            image_urls=[],
            metadata=metadata
        )

    def generate_artist(self) -> Artist:
        source = self.generate_source()
        genres = self.generate_list(self.GENRES)
        metadata = self.generate_metadata()

        return Artist(
            artist_id=ObjectId(),
            source=source,
            name="artist name",
            description="artist description",
            artist_type=random.choice(self.ARTIST_TYPES),
            image_urls=[f"url{i + 1}" for i in range(random.randint(0, 5))],
            listen_count=random.randint(100, 10_000_000),
            tracks={ObjectId(): random.randint(1, 100) for _ in range(random.randint(1, 10))},
            genres=genres,
            metadata=metadata
        )

    def generate_settings(self) -> Settings:
        return Settings(
            username=self.generate_username(),
            show_progress=random.random() < 0.5,
            question_settings=QuestionSettings(
                answer_time=random.randint(150, 450) / 10,
                genres=self.generate_balance(self.GENRES),
                years=self.generate_balance(self.YEARS),
                languages=self.generate_balance(self.LANGUAGES),
                artists_count=self.generate_balance(self.ARTISTS_COUNT),
                listen_count=(random.randint(0, 100), random.randint(1000, 10000)),
                question_types=self.generate_balance(self.QUESTION_TYPES),
                hits=random.choice(self.HITS),
                black_list=[ObjectId() for _ in range(random.randint(0, 10))],
                track_modifications=TrackModificationSettings(
                    change_playback_rate=random.random() < 0.5,
                    probability=random.randint(1, 100) / 100
                ),
                repeat_incorrect_probability=random.randint(1, 100) / 100
            ),
            autoplay=True,
            updated_at=self.generate_datetime()
        )

    def generate_track_landmark(self) -> TrackLandmark:
        return TrackLandmark(
            track_id=ObjectId(),
            timecode=f"{random.randint(0, 100)}-{random.randint(150, 360)}",
            text="landmark text"
        )

    def generate_note(self) -> Note:
        return Note(
            username=self.generate_username(),
            artist_id=ObjectId(),
            text="note text",
            track_landmarks=[self.generate_track_landmark() for _ in range(random.randint(0, 5))]
        )

    def generate_question(self) -> Question:
        return Question(
            username=self.generate_username(),
            question_type=random.choice(self.QUESTION_TYPES),
            group_id=ObjectId(),
            track_id=ObjectId(),
            title="question title",
            answer="question answer",
            question_timecode="0-123",
            question_seek=random.randint(0, 1000) / 10,
            answer_seek=random.randint(0, 1000) / 10,
            track_modifications=TrackModifications(
                playback_rate=random.randint(0, 2) / 10
            ),
            correct=random.random() < 0.5,
            timestamp=self.generate_datetime()
        )
