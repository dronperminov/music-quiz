from datetime import datetime
from typing import List, Tuple

from src import database
from src.entities.quiz_tour import QuizTour
from src.entities.quiz_tour_question import QuizTourQuestion
from src.entities.track import Track
from src.enums import Genre, Language


def tags_to_years(tags: List[str]) -> Tuple[int, int]:
    years = []

    for tag in tags:
        if tag == "1990":
            start_year, end_year = 1990, 1999
        elif tag == "2000":
            start_year, end_year = 2000, 2009
        elif tag == "2010":
            start_year, end_year = 2010, 2019
        elif tag == "2020":
            start_year, end_year = 2020, 2029
        elif tag == "modern":
            start_year, end_year = 2010, datetime.now().year
        else:
            continue

        for year in range(start_year, end_year + 1):
            years.append(year)

    return (0, datetime.now().year) if not years else (min(years), max(years))


def tags_to_languages(tags: List[str]) -> List[Language]:
    languages = []

    if "russian" in tags:
        languages.append(Language.RUSSIAN)

    if "foreign" in tags:
        languages.append(Language.FOREIGN)

    return [Language.RUSSIAN, Language.FOREIGN] if not languages else languages


def tags_to_genres(tags: List[str]) -> List[Genre]:
    genres = []

    if "rock" in tags:
        genres.append(Genre.ROCK)

    if "pop" in tags:
        genres.append(Genre.POP)

    if "hip-hop" in tags:
        genres.append(Genre.HIP_HOP)

    return [Genre.ROCK, Genre.POP, Genre.HIP_HOP, Genre.DISCO, Genre.ELECTRO] if not genres else genres


def main() -> None:
    database.connect()

    for quiz_tour in database.quiz_tours.find({}):
        quiz_tour = QuizTour.from_dict(quiz_tour)
        removing_question_ids = []

        if quiz_tour.name.lower().startswith("любимчики"):
            continue

        languages = tags_to_languages(quiz_tour.tags)
        genres = tags_to_genres(quiz_tour.tags)
        start_year, end_year = tags_to_years(quiz_tour.tags)

        print(f'\nHandle quiz tour "{quiz_tour.name}" ({quiz_tour.quiz_tour_id}):')
        print(f"- tags: {quiz_tour.tags}")
        print(f"- years: {start_year}...{end_year}")
        print(f"- languages: {languages}")
        print(f"- genres: {genres}")

        for question_id in quiz_tour.question_ids:
            question = QuizTourQuestion.from_dict(database.quiz_tour_questions.find_one({"question_id": question_id}))
            track = Track.from_dict(database.tracks.find_one({"track_id": question.question.track_id}))
            artists = ", ".join(artist["name"] for artist in database.artists.find({"artist_id": {"$in": track.artists}}, {"name": 1}))

            if not (start_year <= track.year <= end_year):
                print(f'  - Find invalid track {artists} - "{track.title}" ({track.year} not in [{start_year}, {end_year}])')
                removing_question_ids.append(question_id)
                continue

            if track.language not in languages:
                print(f'  - Find invalid track {artists} - "{track.title}" ({track.language} not in {languages})')
                removing_question_ids.append(question_id)
                continue

            if not set(track.genres).intersection(genres):
                print(f'  - Find invalid track {artists} - "{track.title}" ({track.genres} not in {genres})')
                removing_question_ids.append(question_id)
                continue

        if not removing_question_ids:
            continue

        database.quiz_tour_questions.delete_many({"question_id": {"$in": removing_question_ids}})
        database.quiz_tour_answers.delete_many({"question_id": {"$in": removing_question_ids}})
        quiz_tour.question_ids = [question_id for question_id in quiz_tour.question_ids if question_id not in removing_question_ids]
        database.quiz_tours.update_one({"quiz_tour_id": quiz_tour.quiz_tour_id}, {"$set": quiz_tour.to_dict()})
        print(f"- Removed {len(removing_question_ids)} questions, now: {len(quiz_tour.question_ids)} questions")


if __name__ == "__main__":
    main()
