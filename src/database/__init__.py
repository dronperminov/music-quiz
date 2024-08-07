from src.database.mongo_manager import MongoManager

database = MongoManager(mongo_url="mongodb://localhost:27017/", database_name="music_quiz_db")
