import os
from tempfile import TemporaryDirectory

from tests.database_tests.abstract_music_database_test import AbstractTestMusicDatabase


class TestMusicDatabaseDownload(AbstractTestMusicDatabase):
    tracks_count = 5

    def test_0_init_database(self) -> None:
        tracks, artists = self.music_database.yandex_music_parser.parse_artist(artist_id="160970", max_tracks=self.tracks_count)

        self.music_database.add_from_yandex(artists, tracks, "user")
        self.assertEqual(self.music_database.get_tracks_count(), self.tracks_count)

    def test_1_download_tracks(self) -> None:
        for track_id in range(1, self.tracks_count + 1):
            track = self.music_database.get_track(track_id=track_id)
            self.assertFalse(track.downloaded)

        with TemporaryDirectory() as dir_name:
            self.assertEqual(len(os.listdir(dir_name)), 0)
            self.music_database.download_tracks(output_path=dir_name, username="user")
            filenames = os.listdir(dir_name)

        self.assertEqual(len(filenames), self.tracks_count)

        for track_id in range(1, self.tracks_count + 1):
            track = self.music_database.get_track(track_id=track_id)
            self.assertIn(f"{track_id}.mp3", filenames)
            self.assertTrue(track.downloaded)

    def test_2_download_tracks_image(self) -> None:
        for track_id in range(1, self.tracks_count + 1):
            track = self.music_database.get_track(track_id=track_id)
            self.assertNotEqual(track.image_url, f"/images/tracks/{track_id}.png")

        with TemporaryDirectory() as dir_name:
            self.assertEqual(len(os.listdir(dir_name)), 0)
            self.music_database.download_tracks_image(output_path=dir_name, username="user")
            filenames = os.listdir(dir_name)

        self.assertEqual(len(filenames), self.tracks_count)

        for track_id in range(1, self.tracks_count + 1):
            track = self.music_database.get_track(track_id=track_id)
            self.assertIn(f"{track_id}.png", filenames)
            self.assertEqual(track.image_url, f"/images/tracks/{track_id}.png")

    def test_3_download_artists_images(self) -> None:
        artists_count = self.music_database.get_artists_count()

        for artist_id in range(1, artists_count + 1):
            artist = self.music_database.get_artist(artist_id=artist_id)

            for i, image_url in enumerate(artist.image_urls):
                self.assertNotEqual(image_url, f"/images/artists/{artist_id}/{i}.png")

        with TemporaryDirectory() as dir_name:
            self.assertEqual(len(os.listdir(dir_name)), 0)
            self.music_database.download_artists_images(output_path=dir_name, username="user")
            self.assertEqual(len(os.listdir(dir_name)), artists_count)

            for artist_id in range(1, artists_count + 1):
                artist = self.music_database.get_artist(artist_id=artist_id)
                artist_dir = os.path.join(dir_name, f"{artist.artist_id}")

                self.assertTrue(os.path.isdir(artist_dir))
                self.assertEqual(len(os.listdir(artist_dir)), len(artist.image_urls))

                for i, image_url in enumerate(artist.image_urls):
                    self.assertEqual(image_url, f"/images/artists/{artist_id}/{i}.png")
                    self.assertTrue(os.path.exists(os.path.join(artist_dir, f"{i}.png")))
