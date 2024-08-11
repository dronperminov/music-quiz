import json
import os
import unittest

from src.enums import ArtistType, Genre
from tests.database_tests.abstract_music_database_test import AbstractTestMusicDatabase


class TestMusicDatabaseReal(AbstractTestMusicDatabase):
    @unittest.skip
    def test_0_update_real_data(self) -> None:
        tracks, artists = self.music_database.yandex_music_parser.parse_artist(artist_id="160970", only_sole=True, max_tracks=10)
        with open(os.path.join(self.data_path, "real", "artist_sole.json"), "w", encoding="utf-8") as f:
            json.dump({"yandex_artists": artists, "yandex_tracks": tracks}, f, ensure_ascii=False)

        tracks, artists = self.music_database.yandex_music_parser.parse_artist(artist_id="160970", only_sole=False, max_tracks=10)
        with open(os.path.join(self.data_path, "real", "artist_all.json"), "w", encoding="utf-8") as f:
            json.dump({"yandex_artists": artists, "yandex_tracks": tracks}, f, ensure_ascii=False)

        tracks, artists = self.music_database.yandex_music_parser.parse_playlist(playlist_id="41126", playlist_username="yamusic-bestsongs", max_tracks=4)
        with open(os.path.join(self.data_path, "real", "playlist.json"), "w", encoding="utf-8") as f:
            json.dump({"yandex_artists": artists, "yandex_tracks": tracks}, f, ensure_ascii=False)

        tracks, artists = self.music_database.yandex_music_parser.parse_tracks(track_ids=["40585519", "64355205", "58531281"])
        with open(os.path.join(self.data_path, "real", "tracks.json"), "w", encoding="utf-8") as f:
            json.dump({"yandex_artists": artists, "yandex_tracks": tracks}, f, ensure_ascii=False)

        tracks, artists = self.music_database.yandex_music_parser.parse_chart(max_tracks=100)
        with open(os.path.join(self.data_path, "real", "chart.json"), "w", encoding="utf-8") as f:
            json.dump({"yandex_artists": artists, "yandex_tracks": tracks}, f, ensure_ascii=False)

    def test_1_insert_artist_sole(self) -> None:
        self.add_from_yandex("real/artist_sole.json")
        self.assertEqual(self.music_database.get_artists_count(), 1)
        self.assertEqual(self.music_database.get_tracks_count(), 8)

        artist = self.music_database.get_artist(artist_id=1)
        self.assertEqual(artist.name, "Noize MC")
        self.assertEqual(artist.artist_type, ArtistType.PERFORMER_MALE)
        self.assertEqual(artist.genres, [Genre.HIP_HOP])

    def test_2_insert_artist_all(self) -> None:
        self.add_from_yandex("real/artist_all.json")
        self.assertEqual(self.music_database.get_tracks_count(), 10)
        self.assertEqual(self.music_database.get_artists_count(), 4)

        artist = self.music_database.get_artist(artist_id=3)
        self.assertEqual(artist.name, "Монеточка")
        self.assertEqual(artist.tracks[9], 6)

    def test_3_insert_playlist(self) -> None:
        self.add_from_yandex("real/playlist.json")
        self.assertEqual(self.music_database.get_tracks_count(), 14)
        self.assertEqual(self.music_database.get_artists_count(), 5)

        artist = self.music_database.get_artist(artist_id=5)
        self.assertEqual(artist.name, "Каста")
        self.assertEqual(len(artist.tracks), 4)

    def test_4_insert_tracks(self) -> None:
        self.add_from_yandex("real/tracks.json")
        self.assertEqual(self.music_database.get_tracks_count(), 17)

        artist = self.music_database.get_artist(artist_id=8)
        self.assertEqual(artist.name, "Заточка")
        self.assertEqual(len(artist.tracks), 1)

        track = self.music_database.get_track(track_id=16)
        self.assertEqual(track.title, "Юра, прости")
        self.assertEqual(track.artists, [7])

    def test_5_insert_chart(self) -> None:
        self.add_from_yandex("real/chart.json")
        self.assertEqual(self.music_database.get_tracks_count(), 117)

    def test(self) -> None:
        self.music_database.yandex_music_parser.parse_artist(artist_id="5838706", max_tracks=10)
