import logging
import random
from typing import List

from src import MusicDatabase
from src.database import Database
from src.entities.question import Question
from src.entities.question_settings import QuestionSettings
from src.entities.questions.artist_by_intro_question import ArtistByIntroQuestion
from src.entities.questions.artist_by_track_question import ArtistByTrackQuestion
from src.entities.questions.name_by_track_question import NameByTrackQuestion
from src.entities.settings import Settings
from src.enums import QuestionType


class QuestionsDatabase:
    def __init__(self, database: Database, music_database: MusicDatabase, logger: logging.Logger) -> None:
        self.database = database
        self.music_database = music_database
        self.logger = logger

    def generate_question(self, settings: Settings) -> Question:
        track_ids = self.get_question_track_ids(settings.question_settings)
        track_id = random.choice(track_ids)

        # TODO: statists, balance, etc...
        question_type = random.choice([QuestionType.ARTIST_BY_TRACK, QuestionType.NAME_BY_TRACK])
        question = self.__generate_question_by_type(question_type, track_id, settings)
        return question

    def get_question_track_ids(self, settings: QuestionSettings) -> List[int]:
        possible_track_ids = set()

        for artist in self.database.artists.find(settings.to_artist_query(), {"tracks": 1}):
            possible_track_ids.update(settings.hits.filter_tracks(artist["tracks"]))

        tracks_ids = self.database.tracks.aggregate([
            {"$addFields": {"artists_count": {"$cond": [{"$gt": [{"$size": "$artists"}, 1]}, "feat", "solo"]}}},
            {"$match": {**settings.to_tracks_query(), "track_id": {"$in": list(possible_track_ids)}}},
            {"$project": {"track_id": 1}}
        ])

        return [track["track_id"] for track in tracks_ids]

    def __generate_question_by_type(self, question_type: QuestionType, track_id: int, settings: Settings) -> Question:
        track = self.music_database.get_track(track_id=track_id)
        artist_id2artist = self.music_database.get_track_artists(track=track)

        if question_type == QuestionType.ARTIST_BY_TRACK:
            return ArtistByTrackQuestion(track, artist_id2artist, settings, None)

        if question_type == QuestionType.ARTIST_BY_INTRO:
            return ArtistByIntroQuestion(track, artist_id2artist, settings, None)

        if question_type == QuestionType.NAME_BY_TRACK:
            return NameByTrackQuestion(track, settings, None)

        raise ValueError("Invalid question type")
