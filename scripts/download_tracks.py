from src import database, music_database


def main() -> None:
    output_path = "tracks"
    database.connect()
    music_database.download_tracks(output_path=output_path, username="dronpermninov")


if __name__ == "__main__":
    main()
