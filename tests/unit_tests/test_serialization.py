from datetime import datetime
from unittest import TestCase

from src.entities.artist import Artist
from src.entities.artists_group import ArtistsGroup
from src.entities.artists_group_settings import ArtistsGroupSettings
from src.entities.history_action import AddArtistAction, AddArtistsGroupAction, AddTrackAction, EditArtistAction, EditArtistsGroupAction, EditTrackAction, HistoryAction, \
    RemoveArtistAction, RemoveArtistsGroupAction, RemoveTrackAction
from src.entities.lyrics import Lyrics
from src.entities.lyrics_line import LyricsLine
from src.entities.metadata import Metadata
from src.entities.note import Note
from src.entities.question import ArtistByIntroQuestion, ArtistByTrackQuestion, NameByTrackQuestion, Question
from src.entities.question_settings import QuestionSettings
from src.entities.quiz_tour import QuizTour
from src.entities.quiz_tour_answer import QuizTourAnswer
from src.entities.quiz_tour_question import QuizTourQuestion
from src.entities.settings import Settings
from src.entities.source import HandSource, YandexSource
from src.entities.track import Track
from src.entities.track_modification_settings import TrackModificationSettings
from src.entities.user import User
from src.enums import ArtistType, ArtistsCount, Genre, Language, QuestionType, UserRole
from src.enums import QuizTourType


class TestSerialization(TestCase):
    def __get_track(self) -> Track:
        lyrics = Lyrics(
            lines=[
                LyricsLine(time=0.5, text="line 1"),
                LyricsLine(time=1.3, text="line 2"),
                LyricsLine(time=2.1, text="line 3"),
                LyricsLine(time=6.8, text="line 4"),
            ],
            chorus=[],
            lrc=True,
            validated=True
        )

        return Track(
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
            image_url="url 1",
            metadata=Metadata.initial("system")
        )

    def __get_artist(self, artist_id: int) -> Artist:
        return Artist(
            artist_id=artist_id,
            source=YandexSource(yandex_id="123"),
            name=f"artist {artist_id} name",
            description=f"artist {artist_id} description",
            artist_type=ArtistType.BAND,
            image_urls=["url1", "url2", "url3"],
            listen_count=123000,
            tracks={1: 1, 5: 2, 8: 3},
            tracks_count=10,
            genres=[Genre.ROCK, Genre.POP],
            metadata=Metadata.initial("system")
        )

    def __get_settings(self) -> Settings:
        track_modifications = TrackModificationSettings(
            change_playback_rate=False,
            probability=0
        )

        question_settings = QuestionSettings(
            answer_time=35,
            start_from_chorus=True,
            show_simple_artist_type=True,
            genres={Genre.ROCK: 0.5, Genre.POP: 0.25, Genre.ELECTRO: 0.125, Genre.JAZZ_SOUL: 0.125},
            years={(2020, 2024): 0.25, (1900, 1979): 0.75},
            languages={Language.RUSSIAN: 0.5, Language.FOREIGN: 0.5},
            artists_count={ArtistsCount.SOLO: 1, ArtistsCount.FEAT: 0},
            listen_count=(20000, 100000),
            question_types={QuestionType.ARTIST_BY_TRACK: 0.75, QuestionType.NAME_BY_TRACK: 0.25},
            track_position=(5, ""),
            black_list=[1, 4, 8],
            repeat_incorrect_probability=0.04,
            track_modifications=track_modifications
        )

        artists_group_settings = ArtistsGroupSettings(
            max_variants=4
        )

        return Settings(
            username="user",
            show_progress=True,
            question_settings=question_settings,
            artists_group_settings=artists_group_settings,
            autoplay=True,
            show_knowledge_status=True,
            updated_at=datetime(2024, 1, 1)
        )

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
        artist = self.__get_artist(1)
        artist_dict = artist.to_dict()
        artist_from_dict = Artist.from_dict(artist_dict)
        self.assertEqual(artist, artist_from_dict)

    def test_track_serialization(self) -> None:
        track = self.__get_track()
        track_dict = track.to_dict()
        track_from_dict = Track.from_dict(track_dict)
        self.assertEqual(track, track_from_dict)

    def test_settings_serialization(self) -> None:
        settings = self.__get_settings()
        settings_dict = settings.to_dict()
        settings_from_dict = Settings.from_dict(settings_dict)
        self.assertEqual(settings, settings_from_dict)

    def test_question_serialization(self) -> None:
        track = self.__get_track()
        artist_id2artist = {1: self.__get_artist(1), 3: self.__get_artist(3)}
        settings = self.__get_settings()

        question = ArtistByTrackQuestion.generate(track=track, artist_id2artist=artist_id2artist, username=settings.username, settings=settings.question_settings, group_id=25)
        question_dict = question.to_dict()
        question_from_dict = Question.from_dict(question_dict)
        self.assertEqual(question, question_from_dict)

        question = ArtistByIntroQuestion.generate(track=track, artist_id2artist=artist_id2artist, username=settings.username, settings=settings.question_settings, group_id=25)
        question_dict = question.to_dict()
        question_from_dict = Question.from_dict(question_dict)
        self.assertEqual(question, question_from_dict)

        question = NameByTrackQuestion.generate(track=track, username=settings.username, settings=settings.question_settings, group_id=235)
        question_dict = question.to_dict()
        question_from_dict = Question.from_dict(question_dict)
        self.assertEqual(question, question_from_dict)

    def test_note_serialization(self) -> None:
        note = Note(
            username="system",
            artist_id=4,
            text="note text",
            track_id2seek={1: 40.4, 56: 120.5}
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
            tracks_count=10,
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
            image_url="url 1",
            metadata=Metadata.initial("system")
        )

        group = ArtistsGroup(
            group_id=1,
            name="group name",
            description="group description",
            artist_ids=[1, 2],
            image_url="",
            metadata=Metadata.initial("system")
        )

        history_actions = [
            AddArtistAction(username="system", timestamp=datetime(2024, 1, 1, 20, 23, 51), artist=artist),
            EditArtistAction(username="user", timestamp=datetime(2024, 1, 1, 20, 42, 12), artist_id=artist.artist_id, diff={"name": "aba"}),
            RemoveArtistAction(username="system", timestamp=datetime(2024, 1, 2, 12, 00, 19), artist_id=artist.artist_id),

            AddTrackAction(username="admin", timestamp=datetime(2024, 1, 1, 20, 24, 19), track=track),
            EditTrackAction(username="admin", timestamp=datetime(2024, 1, 1, 20, 54, 11), track_id=track.track_id, diff={"title": "aba"}),
            RemoveTrackAction(username="admin", timestamp=datetime(2024, 5, 1, 0, 0, 0), track_id=track.track_id),

            AddArtistsGroupAction(username="system", timestamp=datetime(2024, 1, 1, 20, 23, 51), group=group),
            EditArtistsGroupAction(username="user", timestamp=datetime(2024, 1, 1, 20, 42, 12), group_id=group.group_id, diff={"name": "aba"}),
            RemoveArtistsGroupAction(username="system", timestamp=datetime(2024, 1, 2, 12, 00, 19), group_id=group.group_id)
        ]

        for history_action in history_actions:
            history_action_dict = history_action.to_dict()
            history_action_from_dict = HistoryAction.from_dict(history_action_dict)
            self.assertEqual(history_action, history_action_from_dict)

    def test_artists_group_serialization(self) -> None:
        group = ArtistsGroup(
            group_id=1,
            name="Some group name",
            description="some group description",
            artist_ids=[1, 5, 123],
            image_url="url",
            metadata=Metadata.initial("user")
        )

        group_dict = group.to_dict()
        group_from_dict = ArtistsGroup.from_dict(group_dict)
        self.assertEqual(group, group_from_dict)

    def test_quiz_tour_serialization(self) -> None:
        quiz_tour = QuizTour(
            quiz_tour_id=1,
            quiz_tour_type=QuizTourType.ALPHABET,
            name="quiz tour name",
            description="quiz tour description",
            question_ids=[1, 5, 8],
            image_url="image url",
            created_at=datetime.now(),
            created_by="user",
            tags=["foreign", "rock"]
        )

        quiz_tour_dict = quiz_tour.to_dict()
        quiz_tour_from_dict = QuizTour.from_dict(quiz_tour_dict)
        self.assertEqual(quiz_tour, quiz_tour_from_dict)

    def test_quiz_tour_question_serialization(self) -> None:
        track = self.__get_track()
        artist_id2artist = {1: self.__get_artist(1), 3: self.__get_artist(3)}
        settings = self.__get_settings()
        question = ArtistByTrackQuestion.generate(track=track, artist_id2artist=artist_id2artist, username=settings.username, settings=settings.question_settings, group_id=35)

        quiz_tour_question = QuizTourQuestion(question_id=1, question=question, answer_time=25)
        quiz_tour_question_dict = quiz_tour_question.to_dict()
        quiz_tour_question_from_dict = QuizTourQuestion.from_dict(quiz_tour_question_dict)
        self.assertEqual(quiz_tour_question, quiz_tour_question_from_dict)

    def test_quiz_tour_answer_serialization(self) -> None:
        answer = QuizTourAnswer(
            question_id=1,
            username="user",
            correct=True,
            timestamp=datetime.now(),
            answer_time=45.25
        )

        answer_dict = answer.to_dict()
        answer_from_dict = QuizTourAnswer.from_dict(answer_dict)
        self.assertEqual(answer, answer_from_dict)
