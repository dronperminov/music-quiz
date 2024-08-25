from dataclasses import dataclass
from datetime import datetime

from src.entities.artist import Artist
from src.entities.artists_group import ArtistsGroup
from src.entities.track import Track


@dataclass
class HistoryAction:
    username: str
    timestamp: datetime

    def __post_init__(self) -> None:
        self.timestamp = self.timestamp.replace(microsecond=0)

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "timestamp": self.timestamp
        }

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

        if name == AddArtistsGroupAction.name:
            return AddArtistsGroupAction(username=username, timestamp=timestamp, group=ArtistsGroup.from_dict(data["group"]))

        if name == EditArtistsGroupAction.name:
            return EditArtistsGroupAction(username=username, timestamp=timestamp, group_id=data["group_id"], diff=data["diff"])

        if name == RemoveArtistsGroupAction.name:
            return RemoveArtistsGroupAction(username=username, timestamp=timestamp, group_id=data["group_id"])

        raise ValueError(f'Invalid HistoryAction name "{name}"')


@dataclass
class AddArtistAction(HistoryAction):
    name = "add_artist"
    artist: Artist

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "artist": self.artist.to_dict()
        }


@dataclass
class EditArtistAction(HistoryAction):
    name = "edit_artist"
    artist_id: int
    diff: dict

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "artist_id": self.artist_id,
            "diff": self.diff
        }


@dataclass
class RemoveArtistAction(HistoryAction):
    name = "remove_artist"
    artist_id: int

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "artist_id": self.artist_id
        }


@dataclass
class AddTrackAction(HistoryAction):
    name = "add_track"
    track: Track

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "track": self.track.to_dict()
        }


@dataclass
class EditTrackAction(HistoryAction):
    name = "edit_track"
    track_id: int
    diff: dict

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "track_id": self.track_id,
            "name": self.name,
            "diff": self.diff
        }


@dataclass
class RemoveTrackAction(HistoryAction):
    name = "remove_track"
    track_id: int

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "track_id": self.track_id
        }


@dataclass
class AddArtistsGroupAction(HistoryAction):
    name = "add_artists_group"
    group: ArtistsGroup

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "group": self.group.to_dict()
        }


@dataclass
class EditArtistsGroupAction(HistoryAction):
    name = "edit_artists_group"
    group_id: int
    diff: dict

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "group_id": self.group_id,
            "diff": self.diff
        }


@dataclass
class RemoveArtistsGroupAction(HistoryAction):
    name = "remove_artists_group"
    group_id: int

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "name": self.name,
            "group_id": self.group_id
        }
