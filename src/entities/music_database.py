import logging
from datetime import datetime
from typing import Dict, List, Optional

from src.database import Database
from src.entities.artist import Artist
from src.entities.history_action import AddArtistAction, AddTrackAction, EditArtistAction, EditTrackAction
from src.entities.metadata import Metadata
from src.entities.source import YandexSource
from src.entities.track import Track


class MusicDatabase:
    def __init__(self, database: Database, logger: logging.Logger) -> None:
        self.database = database
        self.logger = logger

    def get_artist_id(self) -> int:
        identifier = self.database.identifiers.find_one_and_update({"_id": "artists"}, {"$inc": {"value": 1}}, return_document=True)
        return identifier["value"]

    def get_artists_count(self) -> int:
        return self.database.artists.count_documents({})

    def get_artist(self, artist_id: int) -> Optional[Artist]:
        artist = self.database.artists.find_one({"artist_id": artist_id})
        return Artist.from_dict(artist) if artist else None

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

        new_values = {key: key_diff["new"] for key, key_diff in diff.items()}
        action = EditArtistAction(username=username, timestamp=datetime.now(), artist_id=artist_id, diff=diff)
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

        new_values = {key: key_diff["new"] for key, key_diff in diff.items()}
        action = EditTrackAction(username=username, timestamp=datetime.now(), track_id=track_id, diff=diff)
        self.database.tracks.update_one({"track_id": track_id}, {"$set": new_values})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Updated track "{track["title"]}" ({track_id}) by @{username} (keys: {[key for key in diff]})')

    def add_from_yandex(self, artists: List[dict], tracks: List[dict], username: str) -> None:
        yandex2artist_id = {}
        artist_id2yandex_tracks = {}

        for yandex_artist in artists:
            self.__add_yandex_artist(yandex_artist, yandex2artist_id, artist_id2yandex_tracks, username)

        for yandex_track in tracks:
            self.__add_yandex_track(yandex_track, yandex2artist_id, username)

        self.__update_artist_yandex_tracks(artist_id2yandex_tracks, username)

    def __add_yandex_artist(self, yandex_artist: dict, yandex2artist_id: Dict[str, int], artist_id2yandex_tracks: Dict[int, List[str]], username: str) -> None:
        yandex_id: str = yandex_artist["yandex_id"]
        yandex_tracks = yandex_artist.pop("tracks")

        if (artist := self.database.artists.find_one({"source.yandex_id": yandex_id})) is not None:
            artist = Artist.from_dict(artist)
            yandex2artist_id[yandex_id] = artist.artist_id
            artist_id2yandex_tracks[artist.artist_id] = yandex_tracks

            self.logger.info(f"Artist with yandex id = {yandex_id} exists ({artist.name}), try to update")
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
            self.logger.info(f"Track with yandex id = {yandex_id} exists ({track.title}), try to update")
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
