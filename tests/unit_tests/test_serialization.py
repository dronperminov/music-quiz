from bson import ObjectId

from src.entities.artist import Artist
from src.entities.history_action import AddArtistAction, AddTrackAction, EditArtistAction, EditTrackAction, HistoryAction, RemoveArtistAction, RemoveTrackAction
from src.entities.note import Note
from src.entities.question import Question
from src.entities.settings import Settings
from src.entities.track import Track
from src.entities.user import User
from tests.unit_tests.abstract_unit_test import AbstractUnitTest


class TestSerialization(AbstractUnitTest):
    def test_user_serialization(self) -> None:
        user = self.generate_user()
        user_dict = user.to_dict()
        user_from_dict = User.from_dict(user_dict)
        self.assertEqual(user, user_from_dict)

    def test_artist_serialization(self) -> None:
        artist = self.generate_artist()
        artist_dict = artist.to_dict()
        artist_from_dict = Artist.from_dict(artist_dict)
        self.assertEqual(artist, artist_from_dict)

    def test_track_serialization(self) -> None:
        track = self.generate_track(with_lyrics=False)
        track_dict = track.to_dict()
        track_from_dict = Track.from_dict(track_dict)
        self.assertEqual(track, track_from_dict)

        track = self.generate_track(with_lyrics=True)
        track_dict = track.to_dict()
        track_from_dict = Track.from_dict(track_dict)
        self.assertEqual(track, track_from_dict)

    def test_settings_serialization(self) -> None:
        settings = self.generate_settings()
        settings_dict = settings.to_dict()
        settings_from_dict = Settings.from_dict(settings_dict)
        self.assertEqual(settings, settings_from_dict)

    def test_question_serialization(self) -> None:
        question = self.generate_question()
        question_dict = question.to_dict()
        question_from_dict = Question.from_dict(question_dict)
        self.assertEqual(question, question_from_dict)

    def test_note_serialization(self) -> None:
        note = self.generate_note()
        note_dict = note.to_dict()
        note_from_dict = Note.from_dict(note_dict)
        self.assertEqual(note, note_from_dict)

    def test_history_action_serialization(self) -> None:
        history_actions = [
            AddArtistAction(username=self.generate_username(), timestamp=self.generate_datetime(), artist=self.generate_artist()),
            EditArtistAction(username=self.generate_username(), timestamp=self.generate_datetime(), artist_id=ObjectId(), diff={"name": "aba"}),
            RemoveArtistAction(username=self.generate_username(), timestamp=self.generate_datetime(), artist_id=ObjectId()),

            AddTrackAction(username=self.generate_username(), timestamp=self.generate_datetime(), track=self.generate_track()),
            EditTrackAction(username=self.generate_username(), timestamp=self.generate_datetime(), track_id=ObjectId(), diff={"title": "aba"}),
            RemoveTrackAction(username=self.generate_username(), timestamp=self.generate_datetime(), track_id=ObjectId())
        ]

        for history_action in history_actions:
            history_action_dict = history_action.to_dict()
            history_action_from_dict = HistoryAction.from_dict(history_action_dict)
            self.assertEqual(history_action, history_action_from_dict)
