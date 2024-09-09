import re

from src import database, music_database
from src.entities.track import Track
from src.enums import ArtistsCount, Language
from src.query_params.artists_search import ArtistsSearch


def main() -> None:
    database.connect()

    _, artists = music_database.search_artists(params=ArtistsSearch(artists_count={ArtistsCount.SOLO: True}, page_size=4000))

    for artist in artists:
        tracks = [Track.from_dict(track) for track in database.tracks.find({"track_id": {"$in": list(artist.tracks)}})]

        languages = [track.language for track in tracks if track.language != Language.UNKNOWN and len(track.artists) == 1]
        unknown_tracks = [track for track in tracks if track.language == Language.UNKNOWN]

        if not unknown_tracks or len(set(languages)) != 1 or len(languages) < 3:
            continue

        print(f"{artist.name} ({artist.artist_type.to_rus()}): {languages[0]}")
        for track in unknown_tracks:
            music_database.update_track(track_id=track.track_id, diff=track.get_diff({"language": languages[0].value}), username="dronperminov")
        print("")

    for track in database.tracks.find({"language": "unknown"}):
        track = Track.from_dict(track)
        if len(re.findall(r"[а-яА-ЯёЁ]", track.title)) < len(re.findall(r"\w", track.title)) * 0.5:
            continue

        music_database.update_track(track_id=track.track_id, diff=track.get_diff({"language": Language.RUSSIAN.value}), username="dronperminov")


if __name__ == "__main__":
    main()
