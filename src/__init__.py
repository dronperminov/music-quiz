import logging
import sys

from src.database import Database
from src.entities.music_database import MusicDatabase

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

database = Database(mongo_url="mongodb://localhost:27017/", database_name="music_quiz_db")
music_database = MusicDatabase(database=database, logger=logger)
