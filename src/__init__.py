import json
import logging
import os
import sys

from src.database import Database
from src.music_database import MusicDatabase
from src.questions_database import QuestionsDatabase
from src.quiz_tours_database import QuizToursDatabase
from src.utils.yandex_music_parser import YandexMusicParser

secrets_path = os.path.join(os.path.dirname(__file__), "..", "secrets.json")

if os.path.exists(secrets_path):
    with open(secrets_path, "r") as f:
        secrets = json.load(f)
    yandex_music_parser = YandexMusicParser(token=secrets["yandex_token"])
else:
    yandex_music_parser = None

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

database = Database(mongo_url="mongodb://localhost:27017/", database_name="music_quiz_db")
music_database = MusicDatabase(database=database, yandex_music_parser=yandex_music_parser, logger=logger)
questions_database = QuestionsDatabase(database=database, music_database=music_database, logger=logger)
quiz_tours_database = QuizToursDatabase(database=database, questions_database=questions_database, logger=logger)
