import logging
import random
from typing import List, Optional

from src import MusicDatabase
from src.database import Database
from src.entities.question import Question
from src.entities.question_settings import QuestionSettings
from src.entities.questions.artist_by_intro_question import ArtistByIntroQuestion
from src.entities.questions.artist_by_track_question import ArtistByTrackQuestion
from src.entities.questions.name_by_track_question import NameByTrackQuestion
from src.entities.settings import Settings
from src.entities.track import Track
from src.enums import QuestionType
from src.query_params.question_answer import QuestionAnswer


class QuestionsDatabase:
    def __init__(self, database: Database, music_database: MusicDatabase, logger: logging.Logger) -> None:
        self.database = database
        self.music_database = music_database
        self.logger = logger

        self.alpha = 0.99
        self.last_questions_count = 500

    def have_question(self, username: str) -> bool:
        return self.__get_user_question(username=username) is not None

    def answer_question(self, username: str, answer: QuestionAnswer) -> None:
        question = self.__get_user_question(username=username)
        question.set_answer(answer)
        self.database.questions.update_one({"username": username, "correct": None}, {"$set": question.to_dict()})

    def get_question(self, settings: Settings) -> Question:
        tracks = self.get_question_tracks(settings.question_settings)

        if question := self.__get_user_question(username=settings.username):
            if question.track_id in {track["track_id"] for track in tracks}:
                return question

            self.database.questions.delete_one({"username": settings.username, "correct": None})

        last_questions = self.__get_last_questions(username=settings.username)
        last_incorrect_questions = [question for question in last_questions if not question.correct]

        if last_incorrect_questions and random.random() < settings.question_settings.repeat_incorrect_probability:
            question_weights = [1 - self.alpha ** (i + 1) for i in range(len(last_incorrect_questions))]
            question = random.choices(last_incorrect_questions, weights=question_weights, k=1)[0]
            question.remove_answer()
        else:
            question = self.generate_question(tracks, last_questions, settings)

        self.database.questions.insert_one(question.to_dict())
        return question

    def generate_question(self, tracks: List[dict], last_questions: List[Question], settings: Settings) -> Question:
        track = self.get_question_track(tracks=tracks, last_questions=last_questions)

        implemented_question_types = {QuestionType.ARTIST_BY_TRACK, QuestionType.NAME_BY_TRACK, QuestionType.ARTIST_BY_INTRO}
        question_types = list(set(settings.question_settings.question_types).intersection(track.get_question_types()).intersection(implemented_question_types))
        question_weights = [settings.question_settings.question_types[question_type] for question_type in question_types]
        question_type = random.choices(question_types, weights=question_weights, k=1)[0]

        return self.__generate_question_by_type(question_type, track, settings)

    def get_question_track(self, tracks: List[dict], last_questions: List[Question]) -> Track:
        last_track_id2weight = {question.track_id: 1 - self.alpha ** (i + 1) for i, question in enumerate(last_questions)}

        track_weights = [last_track_id2weight.get(track["track_id"], 1) for track in tracks]
        track = random.choices(tracks, weights=track_weights, k=1)[0]
        return self.music_database.get_track(track_id=track["track_id"])

    def get_question_tracks(self, settings: QuestionSettings) -> List[dict]:
        possible_track_ids = set()

        for artist in self.database.artists.find(settings.to_artist_query(), {"tracks": 1}):
            possible_track_ids.update(settings.hits.filter_tracks(artist["tracks"]))

        return list(self.database.tracks.aggregate([
            {"$addFields": {"artists_count": {"$cond": [{"$gt": [{"$size": "$artists"}, 1]}, "feat", "solo"]}}},
            {"$match": {**settings.to_tracks_query(), "track_id": {"$in": list(possible_track_ids)}}},
            {"$project": {"track_id": 1, "genres": 1, "language": 1, "year": 1, "artists_count": 1, "lyrics.lrc": 1, "lyrics.chorus": 1}}
        ]))

    def __generate_question_by_type(self, question_type: QuestionType, track: Track, settings: Settings) -> Question:
        artist_id2artist = self.music_database.get_track_artists(track=track)

        if question_type == QuestionType.ARTIST_BY_TRACK:
            return ArtistByTrackQuestion(track, artist_id2artist, settings, None)

        if question_type == QuestionType.ARTIST_BY_INTRO:
            return ArtistByIntroQuestion(track, artist_id2artist, settings, None)

        if question_type == QuestionType.NAME_BY_TRACK:
            return NameByTrackQuestion(track, settings, None)

        raise ValueError("Invalid question type")

    def __get_user_question(self, username: str) -> Optional[Question]:
        question = self.database.questions.find_one({"username": username, "correct": None})
        return Question.from_dict(question) if question else None

    def __get_last_questions(self, username: str) -> List[Question]:
        last_questions = self.database.questions.find({"username": username, "correct": {"$ne": None}}).sort("timestamp", -1).limit(self.last_questions_count)
        # TODO: check performance, maybe without deserealization
        return [Question.from_dict(question) for question in last_questions]
