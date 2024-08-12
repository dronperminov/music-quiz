import re
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple, Union

from yandex_music import Artist, Client, DownloadInfo, Playlist, Track
from yandex_music.exceptions import NetworkError, NotFoundError

from src.entities.lyrics import Lyrics
from src.enums import ArtistType, Genre, Language


class YandexMusicParser:
    def __init__(self, token: str, covers_size: str = "400x400") -> None:
        self.client = Client(token).init()
        self.covers_size = covers_size

    def get_tracks(self, track_ids: List[str]) -> List[dict]:
        return [self.__process_track(track) for track in self.__request(func=lambda: self.client.tracks(track_ids=track_ids))]

    def parse_tracks(self, track_ids: List[str], only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        tracks = self.get_tracks(track_ids)
        return self.__parse_tracks(tracks, max_tracks=len(tracks), only_sole=only_sole)

    def parse_artist(self, artist_id: str, max_tracks: int, only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        tracks = [self.__process_track(track) for track in self.__request(func=lambda: self.client.artists_tracks(artist_id, page_size=max_tracks))]
        return self.__parse_tracks(tracks, max_tracks=max_tracks, only_sole=only_sole)

    def parse_playlist(self, playlist_id: str, playlist_username: str, max_tracks: int, only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        playlist = self.__request(func=lambda: self.client.users_playlists(playlist_id, playlist_username))
        tracks = [self.__process_track(track.track) for track in playlist.tracks]
        return self.__parse_tracks(tracks, max_tracks=max_tracks, only_sole=only_sole)

    def parse_chart(self, max_tracks: int, only_sole: bool = False) -> Tuple[List[dict], List[dict]]:
        chart = self.__request(func=lambda: self.client.chart())
        tracks = [self.__process_track(track.track) for track in chart.chart.tracks]
        return self.__parse_tracks(tracks, max_tracks=max_tracks, only_sole=only_sole)

    def get_download_info(self, track_ids: List[str], bitrate: int = 192) -> List[DownloadInfo]:
        return [track.get_specific_download_info("mp3", bitrate) for track in self.__request(func=lambda: self.client.tracks(track_ids))]

    def __parse_tracks(self, tracks: List[dict], max_tracks: int, only_sole: bool) -> Tuple[List[dict], List[dict]]:
        if only_sole:
            tracks = [track for track in tracks if len(track["artists"]) == 1]

        tracks = tracks[:max_tracks]

        artist_id2tracks = defaultdict(dict)
        for track in tracks:
            for yandex_artist_id in track["artists"]:
                artist_id2tracks[yandex_artist_id][track["yandex_id"]] = self.__preprocess_title(track["title"])

        artists = [self.__get_artist(yandex_artist_id, track_id2title) for yandex_artist_id, track_id2title in artist_id2tracks.items()]

        track_ids = {track_id for artist in artists for track_id in artist["tracks"]}
        tracks = [track for track in tracks if track["yandex_id"] in track_ids]

        artist2genres = {artist["yandex_id"]: artist["genres"] for artist in artists}
        for track in tracks:
            track["genres"] = self.__get_genres(track, artist2genres)

        return tracks, artists

    def __get_artist(self, artist_id: str, track_id2title: Dict[str, str]) -> dict:
        brief_info = self.__request(func=lambda: self.client._request.get(f"{self.client.base_url}/artists/{artist_id}/brief-info"))
        artist_data = brief_info["artist"]

        listen_count = brief_info.get("stats", {}).get("last_month_listeners", 0)
        description = artist_data["description"]["text"] if "description" in artist_data else ""
        tracks = self.__get_artist_track_positions(artist_id=artist_id, track_id2title=track_id2title)
        genres = [genre.value for genre in set(Genre.from_yandex(genre) for genre in artist_data["genres"]) if genre]

        cover_urls = [f'https://{cover["uri"].replace("%%", self.covers_size)}' for cover in brief_info.get("all_covers", [])]
        if not cover_urls and "cover" in artist_data:
            cover_urls.append(f'https://{artist_data["cover"]["uri"].replace("%%", self.covers_size)}')

        return {
            "yandex_id": artist_id,
            "name": artist_data["name"],
            "artist_type": ArtistType.from_description(description).value,
            "listen_count": listen_count,
            "genres": sorted(genres),
            "description": description,
            "tracks": tracks,
            "tracks_count": artist_data["counts"]["tracks"],
            "image_urls": cover_urls
        }

    def __get_artist_track_positions(self, artist_id: str, track_id2title: Dict[str, str], page_size: int = 20, max_pages: int = 250) -> Dict[str, int]:
        track_id2position = dict()
        title2position = {}

        for page in range(max_pages):
            tracks = self.__request(func=lambda: self.client.artists_tracks(artist_id, page_size=page_size, page=page))  # noqa

            if not tracks:
                break

            for i, track in enumerate(tracks):
                position = page_size * page + i + 1

                if str(track.id) in track_id2title:
                    track_id2position[str(track.id)] = position
                else:
                    title2position[self.__preprocess_title(track.title)] = position

            if len(track_id2position) == len(track_id2title):
                return track_id2position

        # если не нашёлся трек по id, пытаемся найти его по названию
        for track_id, title in track_id2title.items():
            if title in title2position:
                track_id2position[track_id] = title2position[title]

        return track_id2position

    def __process_track(self, track: Track) -> dict:
        lyrics = self.__get_lyrics(track)
        language = lyrics.get_language() if lyrics else Language.UNKNOWN

        return {
            "yandex_id": str(track.id),
            "title": track.title,
            "artists": self.__get_artists(track),
            "year": min([album.year for album in track.albums], default=0),
            "language": language.value,
            "lyrics": lyrics.to_dict() if lyrics else None,
            "duration": round(track.duration_ms / 1000, 2) if track.duration_ms else 0,
            "image_url": track.get_cover_url(self.covers_size) if track.cover_uri else None
        }

    def __get_artists(self, track: Track) -> List[str]:
        artists = []

        for artist in track.artists:
            artists.append(str(artist.id))

            if not artist.decomposed:
                continue

            for decomposed_artist in artist.decomposed:
                if isinstance(decomposed_artist, Artist):
                    artists.append(str(decomposed_artist.id))

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

    def __preprocess_title(self, title: str) -> str:
        title = title.lower()
        title = re.sub(r"^\s+|\s+$|\s*\([^)]+\)\s*$", "", title)
        return title

    def __request(self, func: Callable, max_retries: int = 5) -> Union[dict, list, Playlist]:
        for _ in range(max_retries):
            try:
                return func()
            except NetworkError:
                continue

        raise ValueError("Unable to make request")
