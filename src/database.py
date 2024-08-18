from pymongo import ASCENDING, MongoClient

from src.entities.settings import Settings


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
    similar_artist_groups = None

    def __init__(self, mongo_url: str, database_name: str) -> None:
        self.mongo_url = mongo_url
        self.database_name = database_name

    def connect(self) -> None:
        self.client = MongoClient(self.mongo_url)
        database = self.client[self.database_name]

        self.identifiers = database["identifiers"]

        for name in ["artists", "tracks", "similar_artist_groups"]:
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

        self.similar_artist_groups = database["similar_artist_groups"]
        self.similar_artist_groups.create_index([("group_id", ASCENDING)], unique=True)
        self.similar_artist_groups.create_index([("creator", ASCENDING)])

    def get_settings(self, username: str) -> Settings:
        settings = self.settings.find_one_and_update({"username": username}, {"$setOnInsert": Settings.default(username).to_dict()}, upsert=True, return_document=True)
        return Settings.from_dict(settings)

    def update_settings(self, settings: Settings) -> None:
        self.settings.update_one({"username": settings.username}, {"$set": settings.to_dict()})

    def drop(self) -> None:
        self.client.drop_database(self.database_name)

    def close(self) -> None:
        self.client.close()
