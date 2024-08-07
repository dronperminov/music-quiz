from datetime import datetime
from unittest import TestCase

from src.entities.artist import Artist
from src.entities.history_action import AddArtistAction, AddTrackAction, EditArtistAction, EditTrackAction, HistoryAction, RemoveArtistAction, RemoveTrackAction
from src.entities.lyrics import Lyrics, LyricsLine
from src.entities.metadata import Metadata
from src.entities.note import Note
from src.entities.question import Question
from src.entities.question_settings import QuestionSettings
from src.entities.settings import Settings
from src.entities.source import HandSource, YandexSource
from src.entities.track import Track
from src.entities.track_landmark import TrackLandmark
from src.entities.track_modification_settings import TrackModificationSettings
from src.entities.track_modifications import TrackModifications
from src.entities.user import User
from src.enums import ArtistType, ArtistsCount, Genre, Hits, Language, QuestionType, UserRole


class TestSerialization(TestCase):
    def test_user_serialization(self) -> None:
        user = User(
            username="admin",
            password_hash="password hash",
            full_name="user full name",
            role=UserRole.ADMIN,
            avatar_url="url to avatar"
        )

        user_dict = user.to_dict()
        user_from_dict = User.from_dict(user_dict)
        self.assertEqual(user, user_from_dict)

    def test_artist_serialization(self) -> None:
        artist = Artist(
            artist_id=1,
            source=YandexSource(yandex_id="123"),
            name="artist name",
            description="artist description",
            artist_type=ArtistType.BAND,
            image_urls=["url1", "url2", "url3"],
            listen_count=123000,
            tracks={1: 1, 5: 2, 8: 3},
            genres=[Genre.ROCK, Genre.POP],
            metadata=Metadata.initial("system")
        )

        artist_dict = artist.to_dict()
        artist_from_dict = Artist.from_dict(artist_dict)
        self.assertEqual(artist, artist_from_dict)

    def test_track_serialization(self) -> None:
        lyrics = Lyrics(
            lines=[
                LyricsLine(time=0.5, text="line 1"),
                LyricsLine(time=1.3, text="line 2"),
                LyricsLine(time=2.1, text="line 3"),
                LyricsLine(time=6.8, text="line 4"),
            ],
            chorus=[]
        )

        track = Track(
            track_id=6,
            source=HandSource(),
            title="title",
            artists=[1, 3],
            year=1996,
            lyrics=lyrics,
            genres=[Genre.ROCK],
            language=Language.FOREIGN,
            duration=183.5,
            downloaded=False,
            image_urls=["url 1"],
            metadata=Metadata.initial("system")
        )

        track_dict = track.to_dict()
        track_from_dict = Track.from_dict(track_dict)
        self.assertEqual(track, track_from_dict)

    def test_settings_serialization(self) -> None:
        track_modifications = TrackModificationSettings(
            change_playback_rate=False,
            probability=0
        )

        question_settings = QuestionSettings(
            answer_time=35,
            genres={Genre.ROCK: 0.6, Genre.POP: 0.1, Genre.ELECTRO: 0.2, Genre.JAZZ_SOUL: 0.1},
            years={(2020, 2024): 0.9, (1900, 1979): 0.1},
            languages={Language.RUSSIAN: 0.5, Language.FOREIGN: 0.5},
            artists_count={ArtistsCount.SOLO: 1, ArtistsCount.FEAT: 0},
            listen_count=(20000, 100000),
            question_types={QuestionType.ARTIST_BY_TRACK: 0.75, QuestionType.NAME_BY_TRACK: 0.25},
            hits=Hits.ALL,
            black_list=[1, 4, 8],
            track_modifications=track_modifications,
            repeat_incorrect_probability=0.04
        )

        settings = Settings(
            username="user",
            show_progress=True,
            question_settings=question_settings,
            autoplay=True,
            updated_at=datetime(2024, 1, 1)
        )

        settings_dict = settings.to_dict()
        settings_from_dict = Settings.from_dict(settings_dict)
        self.assertEqual(settings, settings_from_dict)

    def test_question_serialization(self) -> None:
        track_modifications = TrackModifications(
            playback_rate=1
        )

        question = Question(
            username="user",
            question_type=QuestionType.ARTIST_BY_TRACK,
            group_id=245,
            track_id=3,
            title="question title",
            answer="question answer",
            question_timecode="0-123",
            question_seek=5.3,
            answer_seek=None,
            track_modifications=track_modifications,
            correct=None,
            timestamp=datetime(2024, 5, 2, 23, 59)
        )

        question_dict = question.to_dict()
        question_from_dict = Question.from_dict(question_dict)
        self.assertEqual(question, question_from_dict)

    def test_note_serialization(self) -> None:
        track_landmarks = [
            TrackLandmark(track_id=1, timecode="30.2-67", text="landmark text 1"),
            TrackLandmark(track_id=4, timecode="", text="landmark text 2"),
        ]

        note = Note(
            username="system",
            artist_id=4,
            text="note text",
            track_landmarks=track_landmarks
        )

        note_dict = note.to_dict()
        note_from_dict = Note.from_dict(note_dict)
        self.assertEqual(note, note_from_dict)

    def test_history_action_serialization(self) -> None:
        artist = Artist(
            artist_id=1,
            source=YandexSource(yandex_id="123"),
            name="artist name",
            description="artist description",
            artist_type=ArtistType.BAND,
            image_urls=["url1", "url2", "url3"],
            listen_count=123000,
            tracks={1: 1, 6: 2, 8: 3},
            genres=[Genre.ROCK, Genre.POP],
            metadata=Metadata.initial("system")
        )

        track = Track(
            track_id=6,
            source=HandSource(),
            title="title",
            artists=[1],
            year=1996,
            lyrics=None,
            genres=[Genre.ROCK],
            language=Language.FOREIGN,
            duration=183.5,
            downloaded=False,
            image_urls=["url 1"],
            metadata=Metadata.initial("system")
        )

        history_actions = [
            AddArtistAction(username="system", timestamp=datetime(2024, 1, 1, 20, 23, 51), artist=artist),
            EditArtistAction(username="user", timestamp=datetime(2024, 1, 1, 20, 42, 12), artist_id=artist.artist_id, diff={"name": "aba"}),
            RemoveArtistAction(username="system", timestamp=datetime(2024, 1, 2, 12, 00, 19), artist_id=artist.artist_id),

            AddTrackAction(username="admin", timestamp=datetime(2024, 1, 1, 20, 24, 19), track=track),
            EditTrackAction(username="admin", timestamp=datetime(2024, 1, 1, 20, 54, 11), track_id=track.track_id, diff={"title": "aba"}),
            RemoveTrackAction(username="admin", timestamp=datetime(2024, 5, 1, 0, 0, 0), track_id=track.track_id)
        ]

        for history_action in history_actions:
            history_action_dict = history_action.to_dict()
            history_action_from_dict = HistoryAction.from_dict(history_action_dict)
            self.assertEqual(history_action, history_action_from_dict)
