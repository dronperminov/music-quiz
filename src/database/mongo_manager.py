from pymongo import ASCENDING, MongoClient


class MongoManager:
    client: MongoClient = None
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

    def close(self) -> None:
        self.client.close()
