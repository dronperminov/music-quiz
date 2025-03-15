import re
from typing import List, Optional, Tuple

from pymongo import ASCENDING, MongoClient

from src.entities.activity_action import ActivityAction
from src.entities.session import Session
from src.entities.settings import Settings
from src.entities.user import User
from src.enums import UserRole
from src.query_params.activity_search import ActivitySearch


class Database:
    client: MongoClient = None
    identifiers = None
    users = None
    roles = None
    settings = None
    artists = None
    tracks = None
    questions = None
    notes = None
    history = None
    artists_groups = None
    quiz_tours = None
    quiz_tour_questions = None
    quiz_tour_answers = None
    sessions = None

    def __init__(self, mongo_url: str, database_name: str) -> None:
        self.mongo_url = mongo_url
        self.database_name = database_name

    def connect(self) -> None:
        self.client = MongoClient(self.mongo_url)
        database = self.client[self.database_name]

        self.identifiers = database["identifiers"]

        for name in ["artists", "tracks", "artists_groups", "quiz_tours", "quiz_tour_questions"]:
            if self.identifiers.find_one({"_id": name}) is None:
                self.identifiers.insert_one({"_id": name, "value": 0})

        self.users = self.client["quiz"]["users"]
        self.roles = database["roles"]
        self.roles.create_index([("username", ASCENDING)], unique=True)

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

        self.quiz_tours = database["quiz_tours"]
        self.quiz_tours.create_index(([("quiz_tour_id", ASCENDING)]), unique=True)

        self.quiz_tour_questions = database["quiz_tour_questions"]
        self.quiz_tour_questions.create_index(([("question_id", ASCENDING)]), unique=True)

        self.quiz_tour_answers = database["quiz_tour_answers"]
        self.quiz_tour_answers.create_index(([("username", ASCENDING)]))
        self.quiz_tour_answers.create_index(([("correct", ASCENDING)]))

        self.sessions = database["sessions"]
        self.sessions.create_index([("session_id", ASCENDING)], unique=True)

    def get_settings(self, username: str) -> Settings:
        settings = self.settings.find_one_and_update({"username": username}, {"$setOnInsert": Settings.default(username).to_dict()}, upsert=True, return_document=True)
        return Settings.from_dict(settings)

    def update_settings(self, settings: Settings) -> None:
        self.settings.update_one({"username": settings.username}, {"$set": settings.to_dict()})

    def get_user(self, username: str) -> Optional[User]:
        if not username:
            return None

        user: dict = self.users.find_one({"username": {"$regex": f"^{re.escape(username)}$", "$options": "i"}})
        if not user:
            return None

        role = self.roles.find_one({"username": user["username"]})
        return User.from_quiz_dict(user, UserRole(role["role"]) if role else UserRole.USER)

    def get_users(self, usernames: List[str]) -> List[User]:
        users = self.users.find({"username": {"$in": usernames}})
        username2role = {role["username"]: UserRole(role["role"]) for role in self.roles.find({"username": {"$in": usernames}})}
        return [User.from_quiz_dict(user, username2role.get(user["username"], UserRole.USER)) for user in users]

    def get_session(self, session_id: str) -> Optional[Session]:
        session: dict = self.sessions.find_one({"session_id": session_id})
        return Session.from_dict(session) if session else None

    def get_identifier(self, collection_name: str) -> int:
        identifier = self.identifiers.find_one_and_update({"_id": collection_name}, {"$inc": {"value": 1}}, return_document=True)
        return identifier["value"]

    def get_activity(self, params: ActivitySearch) -> Tuple[int, List[ActivityAction]]:
        query = {"correct": {"$ne": None}}
        total = self.questions.count_documents(query)
        questions = self.questions.find(query).sort({"timestamp": -1}).skip(params.page_size * params.page).limit(params.page_size)
        return total, [ActivityAction(username=question["username"], timestamp=question["timestamp"], group_id=question["group_id"]) for question in questions]

    def drop(self) -> None:
        self.client.drop_database(self.database_name)

    def close(self) -> None:
        self.client.close()
