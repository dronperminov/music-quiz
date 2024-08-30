import os
import random
from argparse import ArgumentParser, Namespace
from typing import List

from src import database, quiz_tours_database
from src.entities.question_settings import QuestionSettings
from src.entities.track_modification_settings import TrackModificationSettings
from src.enums import ArtistsCount, Genre, Language, QuestionType
from src.enums import QuizTourType


def get_random_picture(dir_name: str) -> str:
    image_name = random.choice(os.listdir(os.path.join("..", "web", "images", "quiz_tours", dir_name)))
    return f"/images/quiz_tours/{dir_name}/{image_name}"


def get_tags(args: Namespace) -> List[str]:
    tags = []

    if args.languages in ["all", "russian"]:
        tags.append("russian")

    if args.languages in ["all", "foreign"]:
        tags.append("foreign")

    if args.genres != "all":
        tags.append(args.genres)

    if args.positions in ["hits", "unhackneyed"]:
        tags.append(args.positions)

    tags.extend(args.years.split("-") if "-" in args.years else [args.years])
    return tags


def main() -> None:
    parser = ArgumentParser(description="Script for QuizTour generation")
    parser.add_argument("--name", help="Name of the quiz tour", type=str, required=True)
    parser.add_argument("--description", help="Description of the quiz tour", type=str, required=True)
    parser.add_argument("--questions", help="Number of questions", type=int, required=True)
    parser.add_argument("--image", help="Path to dir with image", type=str, required=True)
    parser.add_argument("--years", help="", choices=("1990-2000", "2000", "2000-2010", "modern", "2020"), required=True)
    parser.add_argument("--genres", help="", choices=("all", "rock", "hip-hop"), default="all")
    parser.add_argument("--languages", help="", choices=("all", "russian", "foreign"), default="all")
    parser.add_argument("--positions", help="", choices=("all", "hits", "normal", "unhackneyed"), default="normal")
    parser.add_argument("--mechanics", help="", choices=("regular", "alphabet", "stairs", "letter"), default="regular")
    parser.add_argument("--listen-count", help="Min border of artist listen count", type=int, default=100_000)

    args = parser.parse_args()
    assert args.questions >= 7

    database.connect()

    years = {
        "1990-2000": {(1990, 1999): 1, (2000, 2009): 1},
        "2000": {(2000, 2009): 1},
        "2000-2010": {(2000, 2009): 0.5, (2010, 2019): 0.5},
        "modern": {(2010, 2014): 1, (2015, 2019): 2, (2020, ""): 4},
        "2020": {(2020, ""): 1}
    }[args.years]

    genres = {
        "all": {genre: 1 / len(Genre) for genre in Genre},
        "rock": {Genre.ROCK: 1},
        "hip-hop": {Genre.HIP_HOP: 1}
    }[args.genres]

    languages = {
        "all": {Language.RUSSIAN: 0.5, Language.FOREIGN: 0.5},
        "russian": {Language.RUSSIAN: 1},
        "foreign": {Language.FOREIGN: 1},
    }[args.languages]

    track_position = {
        "all": ("", ""),
        "hits": ("", 5),
        "normal": ("", 10),
        "unhackneyed": (11, "")
    }[args.positions]

    mechanics = {
        "regular": QuizTourType.REGULAR,
        "alphabet": QuizTourType.ALPHABET,
        "stairs": QuizTourType.STAIRS,
        "letter": QuizTourType.LETTER,
    }[args.mechanics]

    settings = QuestionSettings(
        answer_time=0,
        show_simple_artist_type=False,
        start_from_chorus=False,
        genres=genres,
        years=years,
        languages=languages,
        artists_count={ArtistsCount.SOLO: 1},
        listen_count=(args.listen_count, ""),
        question_types={QuestionType.ARTIST_BY_TRACK: 1},
        track_position=track_position,
        black_list=[],
        repeat_incorrect_probability=0,
        track_modifications=TrackModificationSettings(change_playback_rate=False, probability=0)
    )

    params = {
        "name": args.name,
        "description": args.description,
        "image_url": get_random_picture(args.image),
        "tags": get_tags(args)
    }

    print("Generation parameters:")
    print(f'- name: {params["name"]}')
    print(f'- description: {params["description"]}')
    print(f"- questions count: {args.questions}")
    print(f'- image URL: {params["image_url"]}')
    print(f'- tags: {params["tags"]}')
    print(f"- mechanics: {mechanics}\n")

    print("Generation settings:")
    print(f"- years: {settings.years}")
    print(f"- genres: {settings.genres}")
    print(f"- languages: {settings.languages}")
    print(f"- track position: {settings.track_position}")
    print(f"- listen count: {settings.listen_count}")

    answer = input("Write yes for continue >")

    if answer != "yes":
        return

    quiz_tours_database.generate_tour(params, quiz_tour_type=mechanics, settings=settings, questions_count=args.questions)


if __name__ == "__main__":
    main()
