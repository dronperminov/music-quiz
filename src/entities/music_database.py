import logging
from datetime import datetime

from src.database import Database
from src.entities.artist import Artist
from src.entities.history_action import AddArtistAction, AddTrackAction
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

    def add_artist(self, artist: Artist, username: str) -> None:
        action = AddArtistAction(username=username, timestamp=datetime.now(), artist=artist)
        self.database.artists.insert_one(artist.to_dict())
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Added artist "{artist.name}" ({artist.artist_id}) by @{username}')

    def get_track_id(self) -> int:
        identifier = self.database.identifiers.find_one_and_update({"_id": "tracks"}, {"$inc": {"value": 1}}, return_document=True)
        return identifier["value"]

    def get_tracks_count(self) -> int:
        return self.database.tracks.count_documents({})

    def add_track(self, track: Track, username: str) -> None:
        action = AddTrackAction(username=username, timestamp=datetime.now(), track=track)
        self.database.tracks.insert_one(track.to_dict())
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Added track "{track.title}" ({track.track_id}) by @{username}')
