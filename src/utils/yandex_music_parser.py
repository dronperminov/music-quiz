from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

from yandex_music import Artist, Client, DownloadInfo, Track
from yandex_music.exceptions import NotFoundError

from src.entities.lyrics import Lyrics
from src.enums import ArtistType, Genre, Language


class YandexMusicParser:
    def __init__(self, token: str, covers_size: str = "400x400") -> None:
        self.client = Client(token).init()
        self.covers_size = covers_size

    def get_tracks(self, track_ids: List[str]) -> List[dict]:
        return [self.__process_track(track) for track in self.client.tracks(track_ids=track_ids)]

    def parse_tracks(self, track_ids: List[str], only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        tracks = self.get_tracks(track_ids)
        return self.__parse_tracks(tracks, max_tracks=len(tracks), only_sole=only_sole)

    def parse_artist(self, artist_id: str, max_tracks: int, only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        tracks = self.__get_artist_tracks(artist_id=artist_id, max_tracks=max_tracks)
        return self.__parse_tracks(tracks, max_tracks=max_tracks, only_sole=only_sole)

    def parse_playlist(self, playlist_id: str, playlist_username: str, max_tracks: int, only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        playlist = self.client.users_playlists(playlist_id, playlist_username)
        tracks = [self.__process_track(track.track) for track in playlist.tracks]
        return self.__parse_tracks(tracks, max_tracks=max_tracks, only_sole=only_sole)

    def parse_chart(self, max_tracks: int, only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        chart = self.client.chart()
        tracks = [self.__process_track(track.track) for track in chart.chart.tracks]
        return self.__parse_tracks(tracks, max_tracks=max_tracks, only_sole=only_sole)

    def get_download_info(self, track_ids: List[str], bitrate: int = 192) -> List[DownloadInfo]:
        return [track.get_specific_download_info("mp3", bitrate) for track in self.client.tracks(track_ids)]

    def __parse_tracks(self, tracks: List[dict], max_tracks: int, only_sole: bool) -> Tuple[List[dict], List[dict]]:
        if only_sole:
            tracks = [track for track in tracks if len(track["artists"]) == 1]

        tracks = tracks[:max_tracks]

        artist_id2tracks = defaultdict(set)
        for track in tracks:
            for yandex_artist_id in track["artists"]:
                artist_id2tracks[yandex_artist_id].add(track["yandex_id"])

        artists = [self.__get_artist(yandex_artist_id, tracks) for yandex_artist_id, tracks in artist_id2tracks.items()]

        artist2genres = {artist["yandex_id"]: artist["genres"] for artist in artists}
        for track in tracks:
            track["genres"] = self.__get_genres(track, artist2genres)

        return tracks, artists

    def __get_artist(self, artist_id: str, track_ids: Set[str]) -> dict:
        brief_info = self.client._request.get(f"{self.client.base_url}/artists/{artist_id}/brief-info")
        artist_data = brief_info["artist"]

        description = artist_data["description"]["text"] if "description" in artist_data else ""
        tracks = self.__get_artist_track_positions(artist_id=artist_id, track_ids=track_ids)

        artist = self.client.artists([artist_id])[0]
        genres = [genre.value for genre in set(Genre.from_yandex(genre) for genre in artist.genres) if genre]

        cover_urls = [f'https://{cover["uri"].replace("%%", self.covers_size)}' for cover in brief_info.get("all_covers", [])]
        if not cover_urls:
            cover_urls.append(artist.cover.get_url(size=self.covers_size))

        assert {track_id for track_id in tracks} == track_ids  # TODO: remove some tracks

        return {
            "yandex_id": artist_id,
            "name": artist.name,
            "artist_type": ArtistType.from_description(description).value,
            "listen_count": brief_info["stats"]["last_month_listeners"],
            "genres": genres,
            "description": description,
            "tracks": tracks,
            "tracks_count": artist.counts.tracks,
            "image_urls": cover_urls
        }

    def __get_artist_track_positions(self, artist_id: str, track_ids: Set[str], page_size: int = 20, max_pages: int = 250) -> Dict[str, int]:
        track2position = dict()

        for page in range(max_pages):
            tracks = self.client.artists_tracks(artist_id, page_size=page_size, page=page)

            for i, track in enumerate(tracks):
                if track.id in track_ids:
                    track2position[track.id] = page_size * page + i + 1

            if len(track2position) == len(track_ids):
                break

        return track2position

    def __get_artist_tracks(self, artist_id: str, max_tracks: int) -> List[dict]:
        artist_tracks = self.client.artists_tracks(artist_id, page_size=max_tracks)
        tracks = [self.__process_track(track) for track in artist_tracks]
        return tracks[:max_tracks]

    def __process_track(self, track: Track) -> dict:
        lyrics = self.__get_lyrics(track)
        language = lyrics.get_language() if lyrics else Language.UNKNOWN

        return {
            "yandex_id": track.id,
            "title": track.title,
            "artists": self.__get_artists(track),
            "year": min([album.year for album in track.albums], default=0),
            "language": language.value,
            "lyrics": lyrics.to_dict() if lyrics else None,
            "duration": round(track.duration_ms / 1000, 2) if track.duration_ms else 0,
            "image_url": track.get_cover_url(self.covers_size) if track.cover_uri else None
        }

    def __get_artists(self, track: Track) -> List[int]:
        artists = []

        for artist in track.artists:
            artists.append(artist.id)

            if not artist.decomposed:
                continue

            for decomposed_artist in artist.decomposed:
                if isinstance(decomposed_artist, Artist):
                    artists.append(decomposed_artist["id"])

        return artists

    def __get_lyrics(self, track: Track) -> Optional[Lyrics]:
        try:
            return Lyrics.from_lrc(track.get_lyrics("LRC").fetch_lyrics())
        except NotFoundError:
            pass

        try:
            return Lyrics.from_text(track.get_lyrics("TEXT").fetch_lyrics())
        except NotFoundError:
            pass

        return None

    def __get_genres(self, track: dict, artist_id2genres: dict[str, List[str]]) -> List[str]:
        genres = defaultdict(int)

        for artist_id in track["artists"]:
            for genre in artist_id2genres[artist_id]:
                genres[genre] += 1

        max_count = max(genres.values(), default=0)
        return [genre for genre, count in genres.items() if count == max_count]
