from src import database, music_database


def main() -> None:
    database.connect()
    music_database.download_tracks_image(output_path="../web/images/tracks", username="dronperminov")
    music_database.download_artists_images(output_path="../web/images/artists", username="dronperminov")


if __name__ == "__main__":
    main()
