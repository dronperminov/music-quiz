import os
from tempfile import TemporaryDirectory

from tests.database_tests.abstract_music_database_test import AbstractTestMusicDatabase


class TestMusicDatabaseDownload(AbstractTestMusicDatabase):
    def test_download(self) -> None:
        tracks_count = 5
        tracks, artists = self.music_database.yandex_music_parser.parse_artist(artist_id="160970", max_tracks=tracks_count)

        self.music_database.add_from_yandex(artists, tracks, "user")
        self.assertEqual(self.music_database.get_tracks_count(), tracks_count)

        for track_id in range(1, tracks_count + 1):
            track = self.music_database.get_track(track_id=track_id)
            self.assertFalse(track.downloaded)

        with TemporaryDirectory() as dir_name:
            self.assertEqual(len(os.listdir(dir_name)), 0)
            self.music_database.download_tracks(output_path=dir_name, username="user")
            filenames = os.listdir(dir_name)

        self.assertEqual(len(filenames), tracks_count)

        for track_id in range(1, tracks_count + 1):
            track = self.music_database.get_track(track_id=track_id)
            self.assertIn(f"{track_id}.mp3", filenames)
            self.assertTrue(track.downloaded)
