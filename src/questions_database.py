import logging
import random
from collections import defaultdict
from typing import Dict, List, Optional

from src import MusicDatabase
from src.database import Database
from src.entities.artist import Artist
from src.entities.question import ArtistByIntroQuestion, ArtistByTrackQuestion, NameByTrackQuestion, Question
from src.entities.question_settings import QuestionSettings
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

    def have_question(self, username: str, group_id: Optional[int]) -> bool:
        return self.__get_user_question(username=username, group_id=group_id) is not None

    def answer_question(self, username: str, answer: QuestionAnswer) -> None:
        question = self.__get_user_question(username=username, group_id=answer.group_id)
        question.set_answer(answer)
        self.database.questions.update_one({"username": username, "correct": None, "group_id": answer.group_id}, {"$set": question.to_dict()})

    def get_question(self, settings: Settings, group_id: Optional[int] = None) -> Optional[Question]:
        tracks = self.get_question_tracks(settings.question_settings) if group_id is None else self.get_group_question_tracks(group_id)

        if not tracks:
            return None

        if question := self.__get_user_question(username=settings.username, group_id=group_id):
            if question.is_valid({track["track_id"] for track in tracks}, settings):
                return self.__update_question(question, settings)

            self.database.questions.delete_one({"username": settings.username, "correct": None, group_id: group_id})

        last_questions = self.__get_last_questions(username=settings.username, track_ids=[track["track_id"] for track in tracks], group_id=group_id)
        last_incorrect_questions = [question for question in last_questions if not question.correct and question.question_type in settings.question_settings.question_types]

        if last_incorrect_questions and random.random() < settings.question_settings.repeat_incorrect_probability:
            question = self.repeat_incorrect_question(last_incorrect_questions, settings)
        else:
            question = self.generate_question(tracks, last_questions, settings, group_id)

        self.database.questions.insert_one(question.to_dict())
        return question

    def generate_question(self, tracks: List[dict], last_questions: List[Question], settings: Settings, group_id: Optional[int]) -> Question:
        track = self.get_question_track(tracks=tracks, last_questions=last_questions, settings=settings.question_settings, group_id=group_id)

        implemented_question_types = {QuestionType.ARTIST_BY_TRACK, QuestionType.NAME_BY_TRACK, QuestionType.ARTIST_BY_INTRO}
        question_types = list(set(settings.question_settings.question_types).intersection(track.get_question_types()).intersection(implemented_question_types))
        question_weights = [settings.question_settings.question_types[question_type] for question_type in question_types]
        question_type = random.choices(question_types, weights=question_weights, k=1)[0]

        return self.__generate_question_by_type(question_type, track, settings, group_id)

    def repeat_incorrect_question(self, last_incorrect_questions: List[Question], settings: Settings) -> Question:
        question_weights = [1 - self.alpha ** (i + 1) for i in range(len(last_incorrect_questions))]
        question = random.choices(last_incorrect_questions, weights=question_weights, k=1)[0]
        question.remove_answer()
        return self.__update_question(question, settings)

    def get_question_track(self, tracks: List[dict], last_questions: List[Question], settings: QuestionSettings, group_id: Optional[int]) -> Track:
        track_id2weight = {question.track_id: 1 - self.alpha ** (i + 1) for i, question in enumerate(last_questions)}

        if group_id is None:
            feature2balance = {
                "language": {language.value: value for language, value in settings.languages.items()},
                "artists_count": {artists_count.value: value for artists_count, value in settings.artists_count.items()},
                "year_key": {f"{start_year}-{end_year}": value for (start_year, end_year), value in settings.years.items()}
            }

            year2key = settings.get_year2key()
            features2count = defaultdict(int)

            for track in tracks:
                track["year_key"] = year2key[track["year"]]
                features2count[tuple(track[feature] for feature in feature2balance)] += 1

            track_weights = [self.__get_track_weight(track, feature2balance, features2count, track_id2weight) for track in tracks]
        else:
            track_weights = [track_id2weight.get(track["track_id"], 1) for track in tracks]

        track = random.choices(tracks, weights=track_weights, k=1)[0]
        return self.music_database.get_track(track_id=track["track_id"])

    def get_question_tracks(self, settings: QuestionSettings) -> List[dict]:
        possible_track_ids = set()

        for artist in self.database.artists.find(settings.to_artist_query(), {"tracks": 1}):
            possible_track_ids.update(settings.filter_tracks(artist["tracks"]))

        return list(self.database.tracks.aggregate([
            {"$addFields": {"artists_count": {"$cond": [{"$gt": [{"$size": "$artists"}, 1]}, "feat", "solo"]}}},
            {"$match": {**settings.to_tracks_query(), "track_id": {"$in": list(possible_track_ids)}}},
            {"$project": {"track_id": 1, "genres": 1, "language": 1, "year": 1, "artists_count": 1, "lyrics.lrc": 1, "lyrics.chorus": 1}}
        ]))

    def get_group_question_tracks(self, group_id: int) -> List[dict]:
        group = self.database.artists_groups.find_one({"group_id": group_id})
        possible_track_ids = set()

        for artist in self.database.artists.find({"artist_id": {"$in": group["artist_ids"]}}, {"tracks": 1}):
            possible_track_ids.update({track_position["track_id"] for track_position in artist["tracks"]})

        return list(self.database.tracks.aggregate([
            {"$addFields": {"artists_count": {"$cond": [{"$gt": [{"$size": "$artists"}, 1]}, "feat", "solo"]}}},
            {"$match": {"track_id": {"$in": list(possible_track_ids)}, "artists_count": "solo"}},
            {"$project": {"track_id": 1}}
        ]))

    def get_tracks_scales(self, username: str, tracks: List[Track]) -> Dict[int, dict]:
        track_ids = list({track.track_id for track in tracks})
        questions = list(self.database.questions.find({"username": username, "correct": {"$ne": None}, "track_id": {"$in": track_ids}}))
        track_id2scale = {question["track_id"]: {"incorrect": 0, "correct": 0, "scale": 0} for question in questions}

        for question in questions:
            track_id2scale[question["track_id"]]["correct" if question["correct"] else "incorrect"] += 1

        for track_id, scales in track_id2scale.items():
            track_id2scale[track_id]["scale"] = scales["correct"] / (scales["correct"] + scales["incorrect"])

        return track_id2scale

    def get_artists_scales(self, username: str, artists: List[Artist]) -> Dict[int, dict]:
        track_ids = list({track_id for artist in artists for track_id in artist.tracks})
        track_id2scale = {track_id: {False: 0, True: 0} for track_id in track_ids}

        for question in self.database.questions.find({"username": username, "correct": {"$ne": None}, "track_id": {"$in": track_ids}}):
            track_id2scale[question["track_id"]][question["correct"]] += 1

        artist_id2scale = {}
        for artist in artists:
            correct = sum(track_id2scale[track_id][True] for track_id in artist.tracks)
            incorrect = sum(track_id2scale[track_id][False] for track_id in artist.tracks)

            if total := correct + incorrect:
                artist_id2scale[artist.artist_id] = {"correct": correct, "incorrect": incorrect, "scale": correct / total}

        return artist_id2scale

    def __get_track_weight(self, track: dict, feature2balance: Dict[str, Dict[str, float]], features2count: Dict[tuple, float], track_id2weight: Dict[int, float]) -> float:
        track_weight = 1 / features2count[tuple(track[feature] for feature in feature2balance)]

        for feature, feature2value in feature2balance.items():
            track_weight *= feature2value[track[feature]]

        return track_weight * track_id2weight.get(track["track_id"], 1)

    def __generate_question_by_type(self, question_type: QuestionType, track: Track, settings: Settings, group_id: Optional[int]) -> Question:
        artist_id2artist = self.music_database.get_artists_by_ids(artist_ids=track.artists)

        if question_type == QuestionType.ARTIST_BY_TRACK:
            return ArtistByTrackQuestion.generate(track, artist_id2artist, settings, group_id)

        if question_type == QuestionType.ARTIST_BY_INTRO:
            return ArtistByIntroQuestion.generate(track, artist_id2artist, settings, group_id)

        if question_type == QuestionType.NAME_BY_TRACK:
            return NameByTrackQuestion.generate(track, settings, group_id)

        raise ValueError("Invalid question type")

    def __get_user_question(self, username: str, group_id: Optional[int]) -> Optional[Question]:
        question = self.database.questions.find_one({"username": username, "correct": None, "group_id": group_id})
        return Question.from_dict(question) if question else None

    def __get_last_questions(self, username: str, track_ids: List[int], group_id: Optional[int]) -> List[Question]:
        query = {"username": username, "correct": {"$ne": None}, "group_id": group_id, "track_id": {"$in": track_ids}}
        last_questions = self.database.questions.find(query).sort("timestamp", -1).limit(self.last_questions_count)
        return [Question.from_dict(question) for question in last_questions]

    def __update_question(self, question: Question, settings: Settings) -> Question:
        track = self.music_database.get_track(track_id=question.track_id)
        artist_id2artist = self.music_database.get_artists_by_ids(artist_ids=track.artists)
        return question.update(track=track, artist_id2artist=artist_id2artist, settings=settings)
