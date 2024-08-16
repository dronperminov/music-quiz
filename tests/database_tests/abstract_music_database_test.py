import json
import os
from unittest import TestCase

from src import Database, logger, yandex_music_parser
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

    def tearDown(self) -> None:
        self.music_database.validate()

    @classmethod
    def tearDownClass(cls: "AbstractTestMusicDatabase") -> None:
        cls.database.drop()
        cls.database.close()
