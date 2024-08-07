import json
import os
from unittest import TestCase

from src import Database, logger
from src.entities.artist import Artist
from src.entities.metadata import Metadata
from src.entities.music_database import MusicDatabase
from src.entities.source import YandexSource
from src.entities.track import Track
from src.enums import ArtistType, Genre, Language


class TestMusicDatabase(TestCase):
    database: Database
    music_database: MusicDatabase
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")

    @classmethod
    def setUpClass(cls: "TestMusicDatabase") -> None:
        cls.database = Database("mongodb://localhost:27017/", database_name="test_music_quiz_db")
        cls.database.connect()
        cls.music_database = MusicDatabase(database=cls.database, logger=logger)

    def test_1_artist_insert(self) -> None:
        artist = Artist(
            artist_id=self.music_database.get_artist_id(),
            source=YandexSource(yandex_id="123"),
            name="Artist 1",
            description="Some description about artist 1",
            artist_type=ArtistType.PERFORMER_MALE,
            image_urls=["url1"],
            listen_count=125000,
            tracks={},
            genres=[Genre.ROCK],
            metadata=Metadata.initial("system")
        )

        self.assertEqual(self.music_database.get_artists_count(), 0)
        self.music_database.add_artist(artist, artist.metadata.created_by)
        self.assertEqual(self.music_database.get_artists_count(), 1)
        self.assertEqual(artist.artist_id, 1)

        artist_from_db = self.music_database.get_artist(artist.artist_id)
        self.assertIsNotNone(artist_from_db)
        self.assertEqual(artist, artist_from_db)

    def test_2_track_insert(self) -> None:
        artist = self.database.artists.find_one({"source.yandex_id": "123"}, {"artist_id": 1})

        track = Track(
            track_id=self.music_database.get_track_id(),
            source=YandexSource(yandex_id="451"),
            title="Track title",
            artists=[artist["artist_id"]],
            year=2024,
            lyrics=None,
            genres=[Genre.POP, Genre.ROCK],
            language=Language.RUSSIAN,
            duration=124,
            downloaded=False,
            image_urls=["url1"],
            metadata=Metadata.initial("system")
        )

        diff = {"tracks": {"prev": [], "new": [{"track_id": 1, "position": 5}]}}

        self.assertEqual(self.music_database.get_tracks_count(), 0)
        self.music_database.add_track(track, track.metadata.created_by)
        self.music_database.update_artist(artist_id=artist["artist_id"], diff=diff, username=track.metadata.created_by)
        self.assertEqual(self.music_database.get_tracks_count(), 1)
        self.assertEqual(track.track_id, 1)

        track_from_db = self.music_database.get_track(track.track_id)
        self.assertIsNotNone(track_from_db)
        self.assertEqual(track, track_from_db)

    def __add_from_yandex(self, filename: str) -> None:
        with open(os.path.join(self.data_path, filename), encoding="utf-8") as f:
            data = json.load(f)

        self.music_database.add_from_yandex(artists=data["yandex_artists"], tracks=data["yandex_tracks"], username="user")

    def __validate_database(self) -> None:
        for artist in self.database.artists.find({}):
            artist = Artist.from_dict(artist)

            for track_id in artist.tracks:
                track = self.music_database.get_track(track_id)
                self.assertIsNotNone(track)
                self.assertIn(artist.artist_id, track.artists)

        for track in self.database.tracks.find({}):
            track = Track.from_dict(track)

            for artist_id in track.artists:
                artist = self.music_database.get_artist(artist_id)
                self.assertIsNotNone(artist)
                self.assertIn(track.track_id, artist.tracks)

    def test_3_yandex_insert_initial(self) -> None:
        self.__add_from_yandex("yandex_insert_initial.json")

        self.assertEqual(self.music_database.get_artists_count(), 3)
        self.assertEqual(self.music_database.get_tracks_count(), 3)

        artist = self.music_database.get_artist(artist_id=2)
        self.assertIsNotNone(artist)
        self.assertEqual(len(artist.tracks), 2)
        self.assertEqual(artist.tracks[2], 5)
        self.assertEqual(artist.tracks[3], 23)

        artist = self.music_database.get_artist(artist_id=3)
        self.assertIsNotNone(artist)
        self.assertEqual(len(artist.tracks), 1)
        self.assertEqual(artist.name, "RasKar")

        track = self.music_database.get_track(track_id=2)
        self.assertEqual(track.title, "Вселенная бесконечна")
        self.assertEqual(track.year, 2011)
        self.assertEqual(track.duration, 183)

    def test_4_yandex_update_artist(self) -> None:
        self.__add_from_yandex("yandex_update_artist.json")

        self.assertEqual(self.music_database.get_artists_count(), 3)
        self.assertEqual(self.music_database.get_tracks_count(), 3)

        artist = self.music_database.get_artist(artist_id=2)
        self.assertEqual(len(artist.tracks), 2)
        self.assertEqual(artist.listen_count, 2544108)
        self.assertEqual(artist.artist_type, ArtistType.SINGER_MALE)
        self.assertEqual(artist.tracks[2], 5)
        self.assertEqual(artist.tracks[3], 23)

    def test_5_yandex_insert_update(self) -> None:
        self.__add_from_yandex("yandex_insert_update.json")

        self.assertEqual(self.music_database.get_artists_count(), 4)
        self.assertEqual(self.music_database.get_tracks_count(), 5)

        artist = self.music_database.get_artist(artist_id=2)
        self.assertEqual(len(artist.tracks), 3)
        self.assertEqual(artist.listen_count, 2544108)

        artist = self.music_database.get_artist(artist_id=4)
        self.assertEqual(artist.name, "Anacondaz")
        self.assertEqual(artist.artist_type, ArtistType.BAND)

        track = self.music_database.get_track(track_id=2)
        self.assertEqual(track.title, "Вселенная бесконечна")
        self.assertEqual(track.year, 2013)
        self.assertEqual(track.duration, 140)

        track = self.music_database.get_track(track_id=4)
        self.assertEqual(track.title, "Мама, я люблю")
        self.assertEqual(track.year, 2015)
        self.assertEqual(track.duration, 225)

    def test_6_yandex_insert_new_artists(self) -> None:
        self.__add_from_yandex("yandex_insert_new_artists.json")

        self.assertEqual(self.music_database.get_artists_count(), 7)
        self.assertEqual(self.music_database.get_tracks_count(), 5)

    def test_7_yandex_insert_new_tracks(self) -> None:
        self.__add_from_yandex("yandex_insert_new_tracks.json")

        self.assertEqual(self.music_database.get_artists_count(), 7)
        self.assertEqual(self.music_database.get_tracks_count(), 9)

    def tearDown(self) -> None:
        self.__validate_database()

    @classmethod
    def tearDownClass(cls: "TestMusicDatabase") -> None:
        cls.database.drop()
        cls.database.close()
