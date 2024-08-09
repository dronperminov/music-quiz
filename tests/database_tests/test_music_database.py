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

    @classmethod
    def setUpClass(cls: "TestMusicDatabase") -> None:
        cls.database = Database("mongodb://localhost:27017/", database_name="test_music_quiz_db")
        cls.database.connect()
        cls.music_database = MusicDatabase(database=cls.database, logger=logger)

    def test_artist_insert(self) -> None:
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

        artist_from_db = self.database.artists.find_one({"artist_id": artist.artist_id})
        self.assertIsNotNone(artist_from_db)
        self.assertEqual(artist, Artist.from_dict(artist_from_db))

    def test_track_insert(self) -> None:
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

        self.assertEqual(self.music_database.get_tracks_count(), 0)
        self.music_database.add_track(track, track.metadata.created_by)
        self.assertEqual(self.music_database.get_tracks_count(), 1)
        self.assertEqual(track.track_id, 1)

        track_from_db = self.database.tracks.find_one({"track_id": track.track_id})
        self.assertIsNotNone(track_from_db)
        self.assertEqual(track, Track.from_dict(track_from_db))

    @classmethod
    def tearDownClass(cls: "TestMusicDatabase") -> None:
        cls.database.drop()
        cls.database.close()
