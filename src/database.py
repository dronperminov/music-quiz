import re
from typing import Optional

from pymongo import ASCENDING, MongoClient

from src.entities.settings import Settings
from src.entities.user import User


class Database:
    client: MongoClient = None
    identifiers = None
    users = None
    settings = None
    artists = None
    tracks = None
    questions = None
    notes = None
    history = None
    artists_groups = None

    def __init__(self, mongo_url: str, database_name: str) -> None:
        self.mongo_url = mongo_url
        self.database_name = database_name

    def connect(self) -> None:
        self.client = MongoClient(self.mongo_url)
        database = self.client[self.database_name]

        self.identifiers = database["identifiers"]

        for name in ["artists", "tracks", "artists_groups"]:
            if self.identifiers.find_one({"_id": name}) is None:
                self.identifiers.insert_one({"_id": name, "value": 0})

        self.users = database["users"]
        self.users.create_index([("username", ASCENDING)], unique=True)

        self.settings = database["settings"]
        self.settings.create_index([("username", ASCENDING)], unique=True)

        self.artists = database["artists"]
        self.artists.create_index([("artist_id", ASCENDING)], unique=True)
        self.artists.create_index([("name", ASCENDING)])

        self.tracks = database["tracks"]
        self.tracks.create_index([("track_id", ASCENDING)], unique=True)
        self.tracks.create_index([("artists", ASCENDING)])
        self.tracks.create_index([("title", ASCENDING)])
        self.tracks.create_index([("genres", ASCENDING)])
        self.tracks.create_index([("language", ASCENDING)])

        self.questions = database["questions"]
        self.questions.create_index([("username", ASCENDING)])
        self.questions.create_index([("datetime", ASCENDING)])

        self.notes = database["notes"]
        self.notes.create_index([("username", ASCENDING)])
        self.notes.create_index([("artist_id", ASCENDING)])

        self.history = database["history"]
        self.history.create_index([("username", ASCENDING)])
        self.history.create_index([("timestamp", ASCENDING)])

        self.artists_groups = database["artists_groups"]
        self.artists_groups.create_index([("group_id", ASCENDING)], unique=True)
        self.artists_groups.create_index([("creator", ASCENDING)])

    def get_settings(self, username: str) -> Settings:
        settings = self.settings.find_one_and_update({"username": username}, {"$setOnInsert": Settings.default(username).to_dict()}, upsert=True, return_document=True)
        return Settings.from_dict(settings)

    def update_settings(self, settings: Settings) -> None:
        self.settings.update_one({"username": settings.username}, {"$set": settings.to_dict()})

    def get_user(self, username: str) -> Optional[User]:
        if not username:
            return None

        user = self.users.find_one({"username": {"$regex": f"^{re.escape(username)}$", "$options": "i"}})
        return User.from_dict(user) if user else None

    def get_identifier(self, collection_name: str) -> int:
        identifier = self.identifiers.find_one_and_update({"_id": collection_name}, {"$inc": {"value": 1}}, return_document=True)
        return identifier["value"]

    def drop(self) -> None:
        self.client.drop_database(self.database_name)

    def close(self) -> None:
        self.client.close()
