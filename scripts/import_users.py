import re

from pymongo import MongoClient

from src import database, logger, secrets
from src.entities.user import User
from src.enums import UserRole
from src.utils.auth import get_password_hash


def main() -> None:
    database.connect()

    user_roles = {
        "dronperminov": "owner",
        "LittleSun": "owner",
        "sobol": "admin",
        "Lika_Mangova": "admin",
        "alemattoni": "admin",
        "katerinasonrisa": "admin",
        "PaSeR": "admin",
        "Jokogo": "admin"
    }

    client = MongoClient("mongodb://localhost:27017/")

    target_users = [
        User(username="system", password_hash=get_password_hash(secrets["system_password"]), full_name="Система", role=UserRole.OWNER, avatar_url="/profile_images/system.jpg")
    ]

    for user in client["quiz"]["users"].find({}):
        target_users.append(User.from_dict({
            "username": user["username"],
            "password_hash": user["password_hash"],
            "full_name": user["fullname"],
            "avatar_url": user["image_src"],
            "role": user_roles.get(user["username"], "user")
        }))

    for user in target_users:
        db_user = database.users.find_one({"username": {"$regex": f"^{re.escape(user.username)}$", "$options": "i"}})

        if not db_user:
            database.users.insert_one(user.to_dict())
            logger.info(f"Import user @{user.username}")
        elif User.from_dict(db_user) != user:
            database.users.update_one({"username": db_user["username"]}, {"$set": user.to_dict()})
            logger.info(f'Update user @{db_user["username"]} (@{user.username})')


if __name__ == "__main__":
    main()
