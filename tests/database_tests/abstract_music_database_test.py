import json
import os
from unittest import TestCase

from src import Database, logger, yandex_music_parser
from src.entities.artist import Artist
from src.entities.source import YandexSource
from src.entities.track import Track
from src.music_database import MusicDatabase


class AbstractTestMusicDatabase(TestCase):
    database: Database
    music_database: MusicDatabase
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")

    @classmethod
    def setUpClass(cls: "AbstractTestMusicDatabase") -> None:
        cls.database = Database("mongodb://localhost:27017/", database_name="test_music_quiz_db")
        cls.database.connect()
        cls.music_database = MusicDatabase(database=cls.database, yandex_music_parser=yandex_music_parser, logger=logger)

    def add_from_yandex(self, filename: str) -> None:
        with open(os.path.join(self.data_path, filename), encoding="utf-8") as f:
            data = json.load(f)

        self.music_database.add_from_yandex(artists=data["yandex_artists"], tracks=data["yandex_tracks"], username="user")

    def validate_database(self) -> None:
        for artist in self.database.artists.find({}):
            if artist["source"]["name"] == YandexSource.name:
                self.assertTrue(isinstance(artist["source"]["yandex_id"], str))

            artist = Artist.from_dict(artist)

            for track_id in artist.tracks:
                track = self.music_database.get_track(track_id)
                self.assertIsNotNone(track)
                self.assertIn(artist.artist_id, track.artists)

        for track in self.database.tracks.find({}):
            if track["source"]["name"] == YandexSource.name:
                self.assertTrue(isinstance(track["source"]["yandex_id"], str))

            track = Track.from_dict(track)

            for artist_id in track.artists:
                artist = self.music_database.get_artist(artist_id)
                self.assertIsNotNone(artist)
                self.assertIn(track.track_id, artist.tracks)

    def tearDown(self) -> None:
        self.validate_database()

    @classmethod
    def tearDownClass(cls: "AbstractTestMusicDatabase") -> None:
        cls.database.drop()
        cls.database.close()
