import logging
import os
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Set, Tuple

import wget
from pydub import AudioSegment

from src.database import Database
from src.entities.artist import Artist
from src.entities.artists_group import ArtistsGroup
from src.entities.history_action import AddArtistAction, AddArtistsGroupAction, AddNoteAction, AddTrackAction, EditArtistAction, EditArtistsGroupAction, EditNoteAction, \
    EditTrackAction, RemoveArtistAction, RemoveArtistsGroupAction, RemoveTrackAction
from src.entities.metadata import Metadata
from src.entities.note import Note
from src.entities.source import YandexSource
from src.entities.track import Track
from src.enums import ArtistsCount, Language
from src.query_params.artists_groups_search import ArtistsGroupsSearch
from src.query_params.artists_search import ArtistsSearch
from src.utils.yandex_music_parser import YandexMusicParser


class MusicDatabase:
    def __init__(self, database: Database, yandex_music_parser: YandexMusicParser, logger: logging.Logger) -> None:
        self.database = database
        self.yandex_music_parser = yandex_music_parser
        self.logger = logger

    def get_artist_id(self) -> int:
        return self.database.get_identifier("artists")

    def get_artists_count(self) -> int:
        return self.database.artists.count_documents({})

    def get_artist(self, artist_id: int) -> Optional[Artist]:
        artist = self.database.artists.find_one({"artist_id": artist_id})
        return Artist.from_dict(artist) if artist else None

    def search_artists(self, params: ArtistsSearch, username: Optional[str] = None) -> Tuple[int, List[Artist]]:
        results = self.database.artists.aggregate([
            {
                "$addFields": {
                    "name_lowercase": {"$replaceAll": {"input": {"$toLower": "$name"}, "find": "Ё", "replacement": "Е"}},
                    "added_tracks": {"$size": "$tracks"}
                }
            },
            {"$match": self.__get_artists_search_query(params, username)},
            {"$sort": {params.order: params.order_type, "_id": 1}},
            {
                "$facet": {
                    "artists": [{"$skip": params.page_size * params.page}, {"$limit": params.page_size}],
                    "total": [{"$count": "count"}]
                }
            }
        ])

        results = list(results)[0]
        total = 0 if not results["total"] else results["total"][0]["count"]
        return total, [Artist.from_dict(artist) for artist in results["artists"]]

    def get_last_artists(self, order_field: str, order_type: int, count: int, target: str = "all", username: Optional[str] = None) -> List[Artist]:
        _, artists = self.search_artists(ArtistsSearch(order_type=order_type, order=order_field, page_size=count, page=0, target=target), username=username)
        return artists

    def get_artist_tracks(self, artist_id: int) -> List[Track]:
        tracks = self.database.tracks.find({"artists": artist_id})
        return [Track.from_dict(track) for track in tracks]

    def get_artist_names_by_ids(self, artist_ids: List[int]) -> Dict[int, str]:
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

    def remove_artist(self, artist_id: int, username: str) -> None:
        artist = self.database.artists.find_one({"artist_id": artist_id}, {"name": 1, "tracks": 1})
        assert artist is not None

        action = RemoveArtistAction(username=username, timestamp=datetime.now(), artist_id=artist_id)

        for track_position in artist["tracks"]:
            self.remove_track(track_id=track_position["track_id"], username=username, from_artist_id=artist_id)

        for group_data in self.database.artists_groups.find({"artist_ids": artist_id}):
            group = ArtistsGroup.from_dict(group_data)
            group.remove_artist(artist_id)
            diff = ArtistsGroup.from_dict(group_data).get_diff(group.to_dict())
            self.update_artists_group(group_id=group.group_id, diff=diff, username=username)

        self.database.notes.delete_many({"artist_id": artist_id})
        self.database.artists.delete_one({"artist_id": artist_id})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Removed artist "{artist["name"]}" ({artist_id}) by @{username}')

    def get_track_id(self) -> int:
        return self.database.get_identifier("tracks")

    def get_tracks_count(self) -> int:
        return self.database.tracks.count_documents({})

    def get_track(self, track_id: int) -> Optional[Track]:
        track = self.database.tracks.find_one({"track_id": track_id})
        return Track.from_dict(track) if track else None

    def get_artists_by_ids(self, artist_ids: List[int]) -> Dict[int, Artist]:
        return {artist["artist_id"]: Artist.from_dict(artist) for artist in self.database.artists.find({"artist_id": {"$in": artist_ids}})}

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

    def remove_track(self, track_id: int, username: str, from_artist_id: Optional[int] = None) -> None:
        track = self.database.tracks.find_one({"track_id": track_id}, {"title": 1, "artists": 1})
        assert track is not None

        action = RemoveTrackAction(username=username, timestamp=datetime.now(), track_id=track_id)

        for artist_dict in self.database.artists.find({"artist_id": {"$in": track["artists"]}}):
            artist = Artist.from_dict(artist_dict)
            tracks = [track_position for track_position in artist_dict["tracks"] if track_position["track_id"] != track_id]

            if artist.artist_id == from_artist_id:
                continue

            self.update_artist(artist.artist_id, diff=artist.get_diff({"tracks": tracks}), username=username)

            if not tracks:
                self.remove_artist(artist.artist_id, username=username)

        for note_dict in self.database.notes.find({"track_id2seek.track_id": track_id}):
            note = Note.from_dict(note_dict)
            note.track_id2seek.pop(track_id)
            self.database.notes.update_one({"artist_id": note.artist_id, "username": note.username}, {"$set": note.to_dict()})

        self.database.questions.delete_many({"track_id": track_id})
        self.database.tracks.delete_one({"track_id": track_id})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Removed track "{track["title"]}" ({track_id}) by @{username}')

    def download_tracks(self, output_path: str, username: str) -> None:
        tracks = list(self.database.tracks.find({"downloaded": False, "source.name": "yandex"}, {"track_id": 1, "title": 1, "source": 1}))

        for track, info in zip(tracks, self.yandex_music_parser.get_download_info(track_ids=[track["source"]["yandex_id"] for track in tracks])):
            if info is None:
                logging.error(f'Unable download track "{track["title"]}" ({track["track_id"]})')
                continue

            track_path = os.path.join(output_path, f'{track["track_id"]}.mp3')
            info.download(track_path)
            sound = AudioSegment.from_file(track_path)
            sound.export(track_path, format="mp3", bitrate="128k").close()
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

    def get_artists_group_id(self) -> int:
        return self.database.get_identifier("artists_groups")

    def get_artists_group(self, group_id: int) -> Optional[ArtistsGroup]:
        group = self.database.artists_groups.find_one({"group_id": group_id})
        return ArtistsGroup.from_dict(group) if group else None

    def add_artists_group(self, group: ArtistsGroup, username: str) -> None:
        assert self.database.artists.count_documents({"artist_id": {"$in": group.artist_ids}}) == len(group.artist_ids)

        action = AddArtistsGroupAction(username=username, timestamp=datetime.now(), group=group)
        self.database.artists_groups.insert_one(group.to_dict())
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Added artists group "{group.name}" ({group.group_id}) by @{username}')

    def update_artists_group(self, group_id: int, diff: dict, username: str) -> None:
        if not diff:
            return

        group = self.database.artists_groups.find_one({"group_id": group_id}, {"name": 1})
        assert group is not None

        action = EditArtistsGroupAction(username=username, timestamp=datetime.now(), group_id=group_id, diff=diff)

        new_values = {key: key_diff["new"] for key, key_diff in diff.items()}
        new_values["metadata.updated_at"] = action.timestamp
        new_values["metadata.updated_by"] = action.username

        self.database.artists_groups.update_one({"group_id": group_id}, {"$set": new_values})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Updated artists group "{group["name"]}" ({group_id}) by @{username} (keys: {[key for key in diff]})')

    def remove_artists_group(self, group_id: int, username: str) -> None:
        group = self.database.artists_groups.find_one({"group_id": group_id}, {"name": 1, "artist_ids": 1})
        assert group is not None

        action = RemoveArtistsGroupAction(username=username, timestamp=datetime.now(), group_id=group_id)
        self.database.questions.delete_many({"group_id": group_id})
        self.database.artists_groups.delete_one({"group_id": group_id})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Removed artists group "{group["name"]}" ({group_id}) by @{username}')

    def search_artists_groups(self, params: ArtistsGroupsSearch) -> Tuple[int, List[ArtistsGroup]]:
        query = {}
        total = self.database.artists_groups.count_documents(query)
        groups = sorted(self.database.artists_groups.find(query), key=lambda group: (group[params.order], group["group_id"]))
        skip = params.page * params.page_size

        return total, [ArtistsGroup.from_dict(group) for group in groups[skip:skip + params.page_size]]

    def get_groups_tracks_count(self, groups: List[ArtistsGroup]) -> Dict[int, int]:
        group_id2tracks_count = {}

        for group in groups:
            query = {"artists": {"$in": group.artist_ids, "$size": 1}}
            group_id2tracks_count[group.group_id] = self.database.tracks.count_documents(query)

        return group_id2tracks_count

    def get_note(self, artist_id: int, username: str) -> Optional[Note]:
        note = self.database.notes.find_one({"artist_id": artist_id, "username": username})
        return Note.from_dict(note) if note else None

    def add_note(self, note: Note) -> None:
        artist = self.database.artists.find_one({"artist_id": note.artist_id}, {"name": 1})
        assert self.database.notes.find_one({"artist_id": note.artist_id, "username": note.username}) is None
        assert artist is not None

        action = AddNoteAction(username=note.username, timestamp=datetime.now(), note=note)
        self.database.notes.insert_one(note.to_dict())
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f'Added note for artist "{artist["name"]}" ({note.artist_id}) by @{note.username}')

    def update_note(self, note: Note) -> None:
        original_note = self.get_note(artist_id=note.artist_id, username=note.username)
        assert original_note is not None

        if not (diff := original_note.get_diff(note.to_dict())):
            return

        action = EditNoteAction(username=note.username, timestamp=datetime.now(), artist_id=note.artist_id, diff=diff)
        self.database.notes.update_one({"artist_id": note.artist_id, "username": note.username}, {"$set": {key: key_diff["new"] for key, key_diff in diff.items()}})
        self.database.history.insert_one(action.to_dict())

        self.logger.info(f"Updated note for artist {note.artist_id} by @{note.username} (keys: {[key for key in diff]})")

    def add_from_yandex(self, artists: List[dict], tracks: List[dict], username: str) -> Tuple[int, int]:
        yandex2artist_id = {}
        artist_id2yandex_tracks = {}

        artists_count = self.get_artists_count()
        tracks_count = self.get_tracks_count()

        for yandex_artist in artists:
            self.__add_yandex_artist(yandex_artist, yandex2artist_id, artist_id2yandex_tracks, username)

        for yandex_track in tracks:
            self.__add_yandex_track(yandex_track, yandex2artist_id, username)

        self.__update_artist_yandex_tracks(artist_id2yandex_tracks, username)
        return self.get_artists_count() - artists_count, self.get_tracks_count() - tracks_count

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
            assert len(track.artists) > 0, f"track {track.title} ({track.track_id} have no artists"

            for artist_id in track.artists:
                artist = self.get_artist(artist_id)
                assert artist is not None, f"artist {artist_id} is None"
                assert len(artist.tracks) > 0, f'artist "{artist.name}" ({artist.artist_id}) have no tracks'
                assert track.track_id in artist.tracks, f'track "{track.title}" ({track.track_id}) not in artist ({artist.artist_id}) tracks'

    def __get_guessed_artist_ids(self, username: str) -> Set[int]:
        questions = self.database.questions.find({"username": username, "correct": {"$ne": None}}, {"track_id": 1})
        track_ids = {question["track_id"] for question in questions}
        tracks = self.database.tracks.find({"track_id": {"$in": list(track_ids)}}, {"artists": 1})
        return {artist_id for track in tracks for artist_id in track["artists"]}

    def __get_artists_count_artist_ids(self, query: dict, params: ArtistsSearch) -> Tuple[Set[int], Set[int]]:
        artists_count2artist_ids = {enum.value: set() for enum in ArtistsCount}

        for track in self.database.tracks.find({}, {"artists": 1}):
            enum = ArtistsCount.SOLO if len(track["artists"]) == 1 else ArtistsCount.FEAT
            for artist_id in track["artists"]:
                artists_count2artist_ids[enum.value].add(artist_id)

        return params.replace_enum_query(query, artists_count2artist_ids)

    def __get_language_artist_ids(self, query: dict, params: ArtistsSearch) -> Tuple[Set[int], Set[int]]:
        language2artist_ids = {enum.value: set() for enum in Language}

        for track in self.database.tracks.find({}, {"artists": 1, "language": 1}):
            enum = Language(track["language"])
            for artist_id in track["artists"]:
                language2artist_ids[enum.value].add(artist_id)

        return params.replace_enum_query(query, language2artist_ids)

    def __artist_ids_to_query(self, artist_ids_query: Dict[str, Iterable[Set[int]]]) -> dict:
        include_ids = set.intersection(*artist_ids_query["$in"]) if artist_ids_query["$in"] else {}
        exclude_ids = set.union(*artist_ids_query["$nin"]) if artist_ids_query["$nin"] else {}

        if include_ids and exclude_ids:
            return {"$in": list(include_ids.difference(exclude_ids))}

        if include_ids:
            return {"$in": list(include_ids)}

        if exclude_ids:
            return {"$nin": list(exclude_ids)}

        return {}

    def __get_artists_search_query(self, params: ArtistsSearch, username: Optional[str]) -> dict:
        query = params.to_query()
        artist_ids = {"$in": [], "$nin": []}

        if params.target == "questions":
            artist_ids["$in"].append(self.__get_guessed_artist_ids(username))

        if artists_count_query := query.pop("artists_count", {}):
            in_set, nin_set = self.__get_artists_count_artist_ids(artists_count_query, params)
            artist_ids["$in"].append(in_set)
            artist_ids["$nin"].append(nin_set)

        if language_query := query.pop("language", {}):
            in_set, nin_set = self.__get_language_artist_ids(language_query, params)
            artist_ids["$in"].append(in_set)
            artist_ids["$nin"].append(nin_set)

        if artist_ids_query := self.__artist_ids_to_query(artist_ids):
            query["artist_id"] = artist_ids_query

        return query
