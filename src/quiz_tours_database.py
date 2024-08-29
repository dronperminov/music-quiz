import logging
import random
import re
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

from src import Database, QuestionsDatabase
from src.entities.question import Question
from src.entities.question_settings import QuestionSettings
from src.entities.quiz_tour import QuizTour
from src.entities.quiz_tour_answer import QuizTourAnswer
from src.entities.quiz_tour_question import QuizTourQuestion
from src.enums.quiz_tour_type import QuizTourType
from src.query_params.question_answer import QuizTourQuestionAnswer


class QuizToursDatabase:
    def __init__(self, database: Database, questions_database: QuestionsDatabase, logger: logging.Logger) -> None:
        self.database = database
        self.questions_database = questions_database
        self.logger = logger

        self.last_questions_count = 1000

    def get_quiz_tours(self) -> List[QuizTour]:
        return [QuizTour.from_dict(quiz_tour) for quiz_tour in self.database.quiz_tours.find({}).sort("quiz_tour_id", -1)]

    def get_quiz_tour(self, quiz_tour_id: int) -> Optional[QuizTour]:
        quiz_tour = self.database.quiz_tours.find_one({"quiz_tour_id": quiz_tour_id})
        return QuizTour.from_dict(quiz_tour) if quiz_tour else None

    def get_quiz_tour_question(self, username: str, quiz_tour: QuizTour) -> Optional[QuizTourQuestion]:
        answers = list(self.database.quiz_tour_answers.find({"username": username, "question_id": {"$in": quiz_tour.question_ids}}).sort("question_id", -1))

        if len(answers) == len(quiz_tour.question_ids):
            return None

        question = QuizTourQuestion.from_dict(self.database.quiz_tour_questions.find_one({"question_id": quiz_tour.question_ids[len(answers)]}))
        question.question = self.questions_database.update_question(question.question, QuestionSettings.default())
        return question

    def have_question(self, question_id: int, username: str) -> bool:
        if self.database.quiz_tour_questions.find_one({"question_id": question_id}, {"question_id": 1}) is None:
            return False

        if self.database.quiz_tour_answers.find_one({"question_id": question_id, "username": username}) is not None:
            return False

        return True

    def answer_question(self, username: str, answer: QuizTourQuestionAnswer) -> None:
        answer = QuizTourAnswer(question_id=answer.question_id, username=username, correct=answer.correct, timestamp=datetime.now(), answer_time=answer.answer_time)
        self.database.quiz_tour_answers.insert_one(answer.to_dict())

    def get_quiz_tours_statuses(self, username: str, quiz_tours: List[QuizTour]) -> Dict[int, dict]:
        quiz_tour_id2statuses = {}

        for quiz_tour in quiz_tours:
            status = {True: 0, False: 0}

            for answer in self.database.quiz_tour_answers.find({"username": username, "question_id": {"$in": quiz_tour.question_ids}}):
                status[answer["correct"]] += 1

            quiz_tour_id2statuses[quiz_tour.quiz_tour_id] = {"correct": status[True], "incorrect": status[False], "lost": len(quiz_tour.question_ids) - sum(status.values())}

        return quiz_tour_id2statuses

    def generate_tour(self, name: str, description: str, quiz_tour_type: QuizTourType, settings: QuestionSettings, questions_count: int) -> Optional[QuizTour]:
        tracks = self.questions_database.get_question_tracks(settings)

        if len(tracks) < questions_count:
            return None

        last_questions = self.__get_last_questions(track_ids=[track["track_id"] for track in tracks])

        if quiz_tour_type == QuizTourType.REGULAR:
            questions = self.__generate_regular_tour_questions(tracks=tracks, last_questions=last_questions, settings=settings, count=questions_count)
        elif quiz_tour_type == QuizTourType.ALPHABET:
            questions = self.__generate_alphabet_tour_questions(tracks=tracks, last_questions=last_questions, settings=settings, count=questions_count)
        elif quiz_tour_type == QuizTourType.STAIRS:
            questions = self.__generate_stairs_tour_questions(tracks=tracks, last_questions=last_questions, settings=settings, count=questions_count)
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
        questions = []
        sampled_artists = set()

        for _ in range(count):
            track = self.questions_database.sample_question_tracks(tracks, last_questions, settings, None, 1)[0]
            question = self.questions_database.generate_question(track=track, username="", settings=settings, group_id=None)
            questions.append(question)
            last_questions.append(question)

            sampled_artists.update(track.artists)
            tracks = [track for track in tracks if not sampled_artists.intersection(track["artists"])]

        return self.__convert_to_quiz_tour_questions(questions=questions)

    def __generate_alphabet_tour_questions(self, tracks: List[dict], last_questions: List[Question], settings: QuestionSettings, count: int) -> List[QuizTourQuestion]:
        track_ids = {track["track_id"] for track in tracks}
        artists = self.database.artists.find({"tracks.track_id": {"$in": list(track_ids)}}, {"tracks": 1, "name": 1})
        track_id2artist_letter = {}

        for artist in artists:
            for track_position in artist["tracks"]:
                if track_position["track_id"] in track_ids:
                    track_id2artist_letter[track_position["track_id"]] = artist["name"].lower()[0]

        letter2position = {
            "а": 1, "a": 1, "б": 2, "b": 2, "в": 3, "c": 3, "г": 4, "d": 4, "д": 5, "e": 5, "е": 6, "f": 6, "ё": 7, "g": 7, "ж": 8, "h": 8,
            "з": 9, "i": 9, "и": 10, "j": 10, "й": 11, "k": 11, "к": 12, "l": 12, "л": 13, "m": 13, "м": 14, "n": 14, "н": 15, "o": 15,
            "о": 16, "p": 16, "п": 17, "q": 17, "р": 18, "r": 18, "с": 19, "s": 19, "т": 20, "t": 20, "у": 21, "u": 21, "ф": 22, "v": 22,
            "х": 23, "w": 23, "ц": 24, "x": 24, "ч": 25, "y": 25, "ш": 26, "z": 26, "щ": 27, "ъ": 28, "ы": 29, "ь": 30, "э": 31, "ю": 32, "я": 33,
        }

        tracks = [track for track in tracks if track_id2artist_letter[track["track_id"]] in letter2position]

        questions = []
        sampled_letters = set()

        for _ in range(count):
            track = self.questions_database.sample_question_tracks(tracks, last_questions, settings, None, 1)[0]
            question = self.questions_database.generate_question(track=track, username="", settings=settings, group_id=None)
            questions.append(question)
            last_questions.append(question)

            sampled_letters.add(track_id2artist_letter[track.track_id])
            tracks = [track for track in tracks if track_id2artist_letter[track["track_id"]] not in sampled_letters]

        questions = sorted(questions, key=lambda question: letter2position.get(track_id2artist_letter[question.track_id], 100))
        return self.__convert_to_quiz_tour_questions(questions=questions)

    def __generate_stairs_tour_questions(self, tracks: List[dict], last_questions: List[Question], settings: QuestionSettings, count: int) -> List[QuizTourQuestion]:
        track_id2track = {track["track_id"]: track for track in tracks}
        name_len2tracks = defaultdict(list)

        for artist in self.database.artists.find({"tracks.track_id": {"$in": list(track_id2track)}}, {"tracks": 1, "name": 1}):
            name_len = len(re.sub(r"\W", "", artist["name"]))
            for track_position in artist["tracks"]:
                if track_position["track_id"] in track_id2track:
                    name_len2tracks[name_len].append(track_id2track[track_position["track_id"]])

        questions = []
        start_len = random.randint(2, 5)

        for i in range(count):
            track = self.questions_database.sample_question_tracks(name_len2tracks[start_len + i], last_questions, settings, None, 1)[0]
            question = self.questions_database.generate_question(track=track, username="", settings=settings, group_id=None)
            questions.append(question)
            last_questions.append(question)

        return self.__convert_to_quiz_tour_questions(questions=questions)

    def __get_last_questions(self, track_ids: List[int]) -> List[Question]:
        last_questions = self.database.quiz_tour_questions.find({"question.track_id": {"$in": track_ids}}).sort("question_id", -1).limit(self.last_questions_count)
        return [Question.from_dict(question["question"]) for question in last_questions]

    def __convert_to_quiz_tour_questions(self, questions: List[Question], answer_time: float = 45) -> List[QuizTourQuestion]:
        quiz_tour_questions = []

        for question in questions:
            question_id = self.database.get_identifier("quiz_tour_questions")
            tour_question = QuizTourQuestion(question_id=question_id, question=question, answer_time=answer_time)

            self.database.quiz_tour_questions.insert_one(tour_question.to_dict())
            quiz_tour_questions.append(tour_question)

        return quiz_tour_questions
