from src import yandex_music_parser
from src.enums import ArtistType, Genre
from tests.database_tests.abstract_music_database_test import AbstractTestMusicDatabase


class TestMusicDatabase(AbstractTestMusicDatabase):
    def test_1_insert_artist(self) -> None:
        self.assertEqual(self.music_database.get_tracks_count(), 0)
        self.assertEqual(self.music_database.get_artists_count(), 0)

        tracks, artists = yandex_music_parser.parse_artist(artist_id="160970", only_sole=True, max_tracks=10)
        self.music_database.add_from_yandex(artists=artists, tracks=tracks, username="user")
        self.assertEqual(self.music_database.get_artists_count(), 1)
        self.assertEqual(self.music_database.get_tracks_count(), 7)

        artist = self.music_database.get_artist(artist_id=1)
        self.assertEqual(artist.name, "Noize MC")
        self.assertEqual(artist.artist_type, ArtistType.PERFORMER_MALE)
        self.assertEqual(artist.genres, [Genre.HIP_HOP])

        tracks, artists = yandex_music_parser.parse_artist(artist_id="160970", only_sole=False, max_tracks=10)
        self.music_database.add_from_yandex(artists=artists, tracks=tracks, username="user")
        self.assertEqual(self.music_database.get_tracks_count(), 10)
        self.assertEqual(self.music_database.get_artists_count(), 4)

        artist = self.music_database.get_artist(artist_id=3)
        self.assertEqual(artist.name, "Монеточка")
        self.assertEqual(artist.tracks[8], 6)

    def test_2_insert_playlist(self) -> None:
        tracks, artists = yandex_music_parser.parse_playlist(playlist_id="41126", playlist_username="yamusic-bestsongs", max_tracks=4)
        self.music_database.add_from_yandex(artists=artists, tracks=tracks, username="user")
        self.assertEqual(self.music_database.get_tracks_count(), 14)
        self.assertEqual(self.music_database.get_artists_count(), 5)

        artist = self.music_database.get_artist(artist_id=5)
        self.assertEqual(artist.name, "Каста")
        self.assertEqual(len(artist.tracks), 4)

    def test_3_insert_tracks(self) -> None:
        track_ids = ["40585519", "64355205", "58531281"]
        tracks, artists = yandex_music_parser.parse_tracks(track_ids=track_ids)
        self.music_database.add_from_yandex(artists=artists, tracks=tracks, username="user")
        self.assertEqual(self.music_database.get_tracks_count(), 17)

        artist = self.music_database.get_artist(artist_id=8)
        self.assertEqual(artist.name, "Заточка")
        self.assertEqual(len(artist.tracks), 1)

        track = self.music_database.get_track(track_id=16)
        self.assertEqual(track.title, "Юра, прости")
        self.assertEqual(track.artists, [7])

    def test_4_insert_chart(self) -> None:
        tracks, artists = yandex_music_parser.parse_chart(max_tracks=100)
        self.music_database.add_from_yandex(artists=artists, tracks=tracks, username="user")
        self.assertEqual(self.music_database.get_tracks_count(), 117)
