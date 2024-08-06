import abc
from dataclasses import dataclass
from datetime import datetime

from bson import ObjectId

from src.entities.artist import Artist
from src.entities.track import Track


@dataclass
class HistoryAction:
    username: str
    timestamp: datetime

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls: "HistoryAction", data: dict) -> "HistoryAction":
        name = data["name"]
        username = data["username"]
        timestamp = data["timestamp"]

        if name == AddArtistAction.name:
            return AddArtistAction(username=username, timestamp=timestamp, artist=Artist.from_dict(data["artist"]))

        if name == EditArtistAction.name:
            return EditArtistAction(username=username, timestamp=timestamp, artist_id=data["artist_id"], diff=data["diff"])

        if name == RemoveArtistAction.name:
            return RemoveArtistAction(username=username, timestamp=timestamp, artist_id=data["artist_id"])

        if name == AddTrackAction.name:
            return AddTrackAction(username=username, timestamp=timestamp, track=Track.from_dict(data["track"]))

        if name == EditTrackAction.name:
            return EditTrackAction(username=username, timestamp=timestamp, track_id=data["track_id"], diff=data["diff"])

        if name == RemoveTrackAction.name:
            return RemoveTrackAction(username=username, timestamp=timestamp, track_id=data["track_id"])

        raise ValueError(f'Invalid HistoryAction name "{name}"')

    def to_dict_base(self) -> dict:
        return {
            "username": self.username,
            "timestamp": self.timestamp
        }


@dataclass
class AddArtistAction(HistoryAction):
    name = "add_artist"
    artist: Artist

    def to_dict(self) -> dict:
        return {
            **self.to_dict_base(),
            "name": self.name,
            "artist": self.artist.to_dict()
        }


@dataclass
class EditArtistAction(HistoryAction):
    name = "edit_artist"
    artist_id: ObjectId
    diff: dict

    def to_dict(self) -> dict:
        return {
            **self.to_dict_base(),
            "name": self.name,
            "artist_id": self.artist_id,
            "diff": self.diff
        }


@dataclass
class RemoveArtistAction(HistoryAction):
    name = "remove_artist"
    artist_id: ObjectId

    def to_dict(self) -> dict:
        return {
            **self.to_dict_base(),
            "name": self.name,
            "artist_id": self.artist_id
        }


@dataclass
class AddTrackAction(HistoryAction):
    name = "add_track"
    track: Track

    def to_dict(self) -> dict:
        return {
            **self.to_dict_base(),
            "name": self.name,
            "track": self.track.to_dict()
        }


@dataclass
class EditTrackAction(HistoryAction):
    name = "edit_track"
    track_id: ObjectId
    diff: dict

    def to_dict(self) -> dict:
        return {
            **self.to_dict_base(),
            "track_id": self.track_id,
            "name": self.name,
            "diff": self.diff
        }


@dataclass
class RemoveTrackAction(HistoryAction):
    name = "remove_track"
    track_id: ObjectId

    def to_dict(self) -> dict:
        return {
            **self.to_dict_base(),
            "name": self.name,
            "track_id": self.track_id
        }
