import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import wget

from src.database import Database
from src.entities.artist import Artist
from src.entities.history_action import AddArtistAction, AddTrackAction, EditArtistAction, EditTrackAction
from src.entities.metadata import Metadata
from src.entities.source import YandexSource
from src.entities.track import Track
from src.enums import ArtistsCount, Language
from src.query_params.artists_search import ArtistsSearch
from src.utils.yandex_music_parser import YandexMusicParser


class MusicDatabase:
    def __init__(self, database: Database, yandex_music_parser: YandexMusicParser, logger: logging.Logger) -> None:
        self.database = database
        self.yandex_music_parser = yandex_music_parser
        self.logger = logger

    def get_artist_id(self) -> int:
        identifier = self.database.identifiers.find_one_and_update({"_id": "artists"}, {"$inc": {"value": 1}}, return_document=True)
        return identifier["value"]

    def get_artists_count(self) -> int:
        return self.database.artists.count_documents({})

    def get_artist(self, artist_id: int) -> Optional[Artist]:
        artist = self.database.artists.find_one({"artist_id": artist_id})
        return Artist.from_dict(artist) if artist else None

    def search_artists(self, params: ArtistsSearch) -> Tuple[int, List[Artist]]:
        query = params.to_query()

        artist_ids_query = []

        if artists_count_query := query.pop("artists_count", {}):
            artists_count2artist_ids = {enum.value: set() for enum in ArtistsCount}

            for track in self.database.tracks.find({}, {"artists": 1}):
                enum = ArtistsCount.SOLO if len(track["artists"]) == 1 else ArtistsCount.FEAT
                for artist_id in track["artists"]:
                    artists_count2artist_ids[enum.value].add(artist_id)

            artist_ids_query.append(params.replace_enum_query(artists_count_query, artists_count2artist_ids))

        if language_query := query.pop("language", {}):
            language2artist_ids = {enum.value: set() for enum in Language}

            for track in self.database.tracks.find({}, {"artists": 1, "language": 1}):
                enum = Language(track["language"])
                for artist_id in track["artists"]:
                    language2artist_ids[enum.value].add(artist_id)

            artist_ids_query.append(params.replace_enum_query(language_query, language2artist_ids))

        if artist_ids_query:
            query["artist_id"] = {"$in": list(set.intersection(*artist_ids_query))}

        skip = params.page_size * params.page
        total = self.database.artists.count_documents(query)
        artists = self.database.artists.find(query).sort(params.order, params.order_type).skip(skip).limit(params.page_size)
        return total, [Artist.from_dict(artist) for artist in artists]

    def get_last_artists(self, order_field: str, order_type: int, count: int) -> List[Artist]:
        return [Artist.from_dict(artist) for artist in self.database.artists.find({}).sort(order_field, order_type).limit(count)]

    def get_artist_tracks(self, artist_id: int) -> List[Track]:
        tracks = self.database.tracks.find({"artists": artist_id})
        return [Track.from_dict(track) for track in tracks]

    def get_artist_names(self, tracks: List[Track]) -> Dict[int, str]:
        artist_ids = set()

        for track in tracks:
            artist_ids.update(track.artists)

        artists = self.database.artists.find({"artist_id": {"$in": list(artist_ids)}}, {"artist_id": 1, "name": 1})
        return {artist["artist_id"]: artist["name"] for artist in artists}

    def add_artist(self, artist: Artist, username: str) -> None:
        action = AddArtistAction(username=username, timestamp=datetime.now(), artist=artist)
        self.database.artists.insert_one(artist.to_dict())
        self.database.history.insert_one(action.to_dict())

        # TODO: download images
        self.logger.info(f'Added artist "{artist.name}" ({artist.artist_id}) by @{username}')

    def update_artist(self, artist_id: int, diff: dict, username: str) -> None:
        if not diff:
            return

        artist = self.database.artists.find_one({"artist_id": artist_id}, {"name": 1})
        assert artist is not None

        action = EditArtistAction(username=username, timestamp=datetime.now(), artist_id=artist_id, diff=diff)

        new_values = {key: key_diff["new"] for key, key_diff in diff.items()}
        new_values["metadata.updated_at"] = action.timestamp
        new_values["metadata.updated_by"] = action.username

        self.database.artists.update_one({"artist_id": artist_id}, {"$set": new_values})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Updated artist "{artist["name"]}" ({artist_id}) by @{username} (keys: {[key for key in diff]})')

    def get_track_id(self) -> int:
        identifier = self.database.identifiers.find_one_and_update({"_id": "tracks"}, {"$inc": {"value": 1}}, return_document=True)
        return identifier["value"]

    def get_tracks_count(self) -> int:
        return self.database.tracks.count_documents({})

    def get_track(self, track_id: int) -> Optional[Track]:
        track = self.database.tracks.find_one({"track_id": track_id})
        return Track.from_dict(track) if track else None

    def add_track(self, track: Track, username: str) -> None:
        assert self.database.artists.count_documents({"artist_id": {"$in": track.artists}}) == len(track.artists)

        action = AddTrackAction(username=username, timestamp=datetime.now(), track=track)
        self.database.tracks.insert_one(track.to_dict())
        self.database.history.insert_one(action.to_dict())

        # TODO: download images and audio
        self.logger.info(f'Added track "{track.title}" ({track.track_id}) by @{username}')

    def update_track(self, track_id: int, diff: dict, username: str) -> None:
        if not diff:
            return

        track = self.database.tracks.find_one({"track_id": track_id}, {"title": 1})
        assert track is not None

        action = EditTrackAction(username=username, timestamp=datetime.now(), track_id=track_id, diff=diff)

        new_values = {key: key_diff["new"] for key, key_diff in diff.items()}
        new_values["metadata.updated_at"] = action.timestamp
        new_values["metadata.updated_by"] = action.username

        self.database.tracks.update_one({"track_id": track_id}, {"$set": new_values})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Updated track "{track["title"]}" ({track_id}) by @{username} (keys: {[key for key in diff]})')

    def download_tracks(self, output_path: str, username: str) -> None:
        tracks = list(self.database.tracks.find({"downloaded": False, "source.name": "yandex"}, {"track_id": 1, "source": 1}))

        for track, info in zip(tracks, self.yandex_music_parser.get_download_info(track_ids=[track["source"]["yandex_id"] for track in tracks])):
            info.download(os.path.join(output_path, f'{track["track_id"]}.mp3'))
            self.update_track(track_id=track["track_id"], diff={"downloaded": {"prev": False, "new": True}}, username=username)

    def download_tracks_image(self, output_path: str, username: str) -> None:
        for track in self.database.tracks.find({"image_url": {"$ne": None, "$not": {"$regex": "^/images/tracks/.*"}}}, {"track_id": 1, "image_url": 1}):
            wget.download(track["image_url"], os.path.join(output_path, f'{track["track_id"]}.png'))
            diff = {"image_url": {"prev": track["image_url"], "new": f'/images/tracks/{track["track_id"]}.png'}}
            self.update_track(track_id=track["track_id"], diff=diff, username=username)

    def download_artists_images(self, output_path: str, username: str) -> None:
        for artist in self.database.artists.find({"image_urls": {"$ne": [], "$not": {"$regex": "^/images/artists/.*"}}}, {"artist_id": 1, "image_urls": 1}):
            artist_dir = os.path.join(output_path, f'{artist["artist_id"]}')
            os.makedirs(artist_dir, exist_ok=True)
            image_urls = []

            for i, image_url in enumerate(artist["image_urls"]):
                wget.download(image_url, os.path.join(artist_dir, f"{i}.png"))
                image_urls.append(f'/images/artists/{artist["artist_id"]}/{i}.png')

            diff = {"image_urls": {"prev": artist["image_urls"], "new": image_urls}}
            self.update_artist(artist_id=artist["artist_id"], diff=diff, username=username)

    def add_from_yandex(self, artists: List[dict], tracks: List[dict], username: str) -> None:
        yandex2artist_id = {}
        artist_id2yandex_tracks = {}

        for yandex_artist in artists:
            self.__add_yandex_artist(yandex_artist, yandex2artist_id, artist_id2yandex_tracks, username)

        for yandex_track in tracks:
            self.__add_yandex_track(yandex_track, yandex2artist_id, username)

        self.__update_artist_yandex_tracks(artist_id2yandex_tracks, username)

    def validate(self) -> None:
        self.__validate_artists()
        self.__validate_tracks()

    def __add_yandex_artist(self, yandex_artist: dict, yandex2artist_id: Dict[str, int], artist_id2yandex_tracks: Dict[int, List[str]], username: str) -> None:
        yandex_id: str = yandex_artist["yandex_id"]
        yandex_tracks = yandex_artist.pop("tracks")

        if (artist := self.database.artists.find_one({"source.yandex_id": yandex_id})) is not None:
            artist = Artist.from_dict(artist)
            yandex2artist_id[yandex_id] = artist.artist_id
            artist_id2yandex_tracks[artist.artist_id] = yandex_tracks
            self.update_artist(artist_id=artist.artist_id, diff=artist.get_diff(yandex_artist), username=username)
            return

        artist_id = self.get_artist_id()
        artist_id2yandex_tracks[artist_id] = yandex_tracks
        artist = Artist.from_dict({
            **yandex_artist,
            "artist_id": artist_id,
            "source": YandexSource(yandex_id=yandex_id).to_dict(),
            "tracks": {},
            "metadata": Metadata.initial(username=username).to_dict()
        })

        yandex2artist_id[yandex_id] = artist.artist_id
        self.add_artist(artist=artist, username=username)

    def __add_yandex_track(self, yandex_track: dict, yandex2artist_id: Dict[str, int], username: str) -> None:
        yandex_id: str = yandex_track["yandex_id"]
        yandex_track["artists"] = [yandex2artist_id[yandex_artist_id] for yandex_artist_id in yandex_track["artists"]]

        if (track := self.database.tracks.find_one({"source.yandex_id": yandex_id})) is not None:
            track = Track.from_dict(track)
            self.update_track(track_id=track.track_id, diff=track.get_diff(yandex_track), username=username)
            return

        track = Track.from_dict({
            **yandex_track,
            "track_id": self.get_track_id(),
            "source": YandexSource(yandex_id=yandex_id).to_dict(),
            "downloaded": False,
            "metadata": Metadata.initial(username=username).to_dict()
        })

        self.add_track(track=track, username=username)

    def __update_artist_yandex_tracks(self, artist_id2yandex_tracks: Dict[int, dict], username: str) -> None:
        for artist_id, yandex_tracks in artist_id2yandex_tracks.items():
            track_ids = set()
            tracks = []

            for yandex_id, position in yandex_tracks.items():
                track_id = self.database.tracks.find_one({"source.yandex_id": yandex_id}, {"track_id": 1})["track_id"]
                tracks.append({"track_id": track_id, "position": position})
                track_ids.add(track_id)

            artist = self.get_artist(artist_id)
            tracks.extend([track_data for track_data in artist.get_tracks_dict() if track_data["track_id"] not in track_ids])
            self.update_artist(artist_id=artist_id, diff=artist.get_diff({"tracks": tracks}), username=username)

    def __validate_artists(self) -> None:
        for artist in self.database.artists.find({}):
            if artist["source"]["name"] == YandexSource.name:
                assert isinstance(artist["source"]["yandex_id"], str)

            artist = Artist.from_dict(artist)

            for track_id in artist.tracks:
                track = self.get_track(track_id)
                assert track is not None, f"track {track_id} is None"
                assert len(track.artists) > 0, f'track "{track.title}" ({track.track_id}) have no artists'
                assert artist.artist_id in track.artists, f'artist "{artist.name}" ({artist.artist_id}) not in track ({track.track_id}) artists'

    def __validate_tracks(self) -> None:
        for track in self.database.tracks.find({}):
            if track["source"]["name"] == YandexSource.name:
                assert isinstance(track["source"]["yandex_id"], str)

            track = Track.from_dict(track)

            for artist_id in track.artists:
                artist = self.get_artist(artist_id)
                assert artist is not None, f"artist {artist_id} is None"
                assert len(artist.tracks) > 0, f'artist "{artist.name}" ({artist.artist_id}) have no tracks'
                assert track.track_id in artist.tracks, f'track "{track.title}" ({track.track_id}) not in artist ({artist.artist_id}) tracks'
