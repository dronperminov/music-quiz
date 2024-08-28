import logging
from datetime import datetime
from typing import List, Optional

from src import Database, QuestionsDatabase
from src.entities.question import Question
from src.entities.question_settings import QuestionSettings
from src.entities.quiz_tour import QuizTour
from src.entities.quiz_tour_question import QuizTourQuestion
from src.entities.track import Track
from src.enums.quiz_tour_type import QuizTourType


class QuizToursDatabase:
    def __init__(self, database: Database, questions_database: QuestionsDatabase, logger: logging.Logger) -> None:
        self.database = database
        self.questions_database = questions_database
        self.logger = logger

        self.last_questions_count = 1000

    def get_quiz_tours(self) -> List[QuizTour]:
        return [QuizTour.from_dict(quiz_tour) for quiz_tour in self.database.quiz_tours.find({}).sort("quiz_tour_id", -1)]

    def generate_tour(self, name: str, description: str, quiz_tour_type: QuizTourType, settings: QuestionSettings, questions_count: int) -> Optional[QuizTour]:
        tracks = self.questions_database.get_question_tracks(settings)
        if len(tracks) < questions_count:
            return None

        last_questions = self.__get_last_questions(track_ids=[track["track_id"] for track in tracks])

        if quiz_tour_type == QuizTourType.REGULAR:
            questions = self.__generate_regular_tour_questions(tracks=tracks, last_questions=last_questions, settings=settings, count=questions_count)
        elif quiz_tour_type == QuizTourType.ALPHABET:
            questions = self.__generate_alphabet_tour_questions(tracks=tracks, last_questions=last_questions, settings=settings, count=questions_count)
        else:
            raise ValueError(f'Invalid quiz tour type "{quiz_tour_type}"')

        quiz_tour = QuizTour(
            quiz_tour_id=self.database.get_identifier("quiz_tours"),
            quiz_tour_type=quiz_tour_type,
            name=name,
            description=description,
            question_ids=[question.question_id for question in questions],
            image_url="/images/quiz_tours/default.png",
            created_at=datetime.now(),
            created_by="system"
        )
        self.database.quiz_tours.insert_one(quiz_tour.to_dict())
        return quiz_tour

    def __generate_regular_tour_questions(self, tracks: List[dict], last_questions: List[Question], settings: QuestionSettings, count: int) -> List[QuizTourQuestion]:
        tracks = self.questions_database.sample_question_tracks(tracks, last_questions, settings, None, count)
        return self.__tracks_to_questions(tracks=tracks, settings=settings)

    def __generate_alphabet_tour_questions(self, tracks: List[dict], last_questions: List[Question], settings: QuestionSettings, count: int) -> List[QuizTourQuestion]:
        tracks = self.questions_database.sample_question_tracks(tracks, last_questions, settings, None, count)
        tracks = sorted(tracks, key=lambda track: track.title.lower())
        return self.__tracks_to_questions(tracks=tracks, settings=settings)

    def __get_last_questions(self, track_ids: List[int]) -> List[Question]:
        last_questions = self.database.quiz_tour_questions.find({"question.track_id": {"$in": track_ids}}).sort("question_id", -1).limit(self.last_questions_count)
        return [Question.from_dict(question["question"]) for question in last_questions]

    def __tracks_to_questions(self, tracks: List[Track], settings: QuestionSettings, answer_time: float = 45) -> List[QuizTourQuestion]:
        questions = []
        artist_ids = set()

        for track in tracks:
            # TODO: sample tracks accurate and remove this check
            assert len(track.artists) == 1
            assert track.artists[0] not in artist_ids
            artist_ids.add(track.artists[0])

            question_id = self.database.get_identifier("quiz_tour_questions")
            question = self.questions_database.generate_question(track=track, username="", settings=settings, group_id=None)
            tour_question = QuizTourQuestion(question_id=question_id, question=question, answer_time=answer_time)

            self.database.quiz_tour_questions.insert_one(tour_question.to_dict())
            questions.append(tour_question)

        return questions
