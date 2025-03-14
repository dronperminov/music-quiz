import os
import random
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import database, music_database, questions_database, quiz_tours_database
from src.api import login_redirect, send_error, templates
from src.entities.user import User
from src.enums import QuizTourType, UserRole
from src.query_params.question_answer import QuizTourQuestionAnswer
from src.query_params.quiz_tour_add import QuizTourAdd
from src.query_params.quiz_tours_search import QuizToursSearch, QuizToursSearchQuery
from src.utils.auth import get_user
from src.utils.common import format_time, get_name_length, get_static_hash, get_top_letter, get_word_form

router = APIRouter()


@router.get("/quiz-tours")
def get_quiz_tours(params: QuizToursSearchQuery = Depends(), user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    template = templates.get_template("quiz_tours/quiz_tours.html")
    content = template.render(
        user=user,
        page="quiz_tours",
        version=get_static_hash(),
        search_params=params.to_params(user is not None),
        QuizTourType=QuizTourType
    )
    return HTMLResponse(content=content)


@router.get("/quiz-tour/{quiz_tour_id}")
def get_quiz_tour(quiz_tour_id: int, user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return login_redirect(back_url=f"/quiz-tours/{quiz_tour_id}")

    quiz_tour = quiz_tours_database.get_quiz_tour(quiz_tour_id=quiz_tour_id)

    if not quiz_tour:
        return send_error(user=user, title="Запрашиваемый квиз не существует", text="Не удалось найти запрашиваемый квиз. Возможно, он был удалён или ещё не был создан.")

    if not quiz_tours_database.is_tour_ended(username=user.username, quiz_tour=quiz_tour):
        return RedirectResponse(f"/quiz-tours/{quiz_tour_id}")

    settings = database.get_settings(username=user.username)
    statuses = quiz_tours_database.get_quiz_tours_statuses(username=user.username, quiz_tours=[quiz_tour])
    track_id2status = quiz_tours_database.get_quiz_tour_tracks_statuses(quiz_tour=quiz_tour)
    track_id2correct = quiz_tours_database.get_quiz_tour_track_results(username=user.username, quiz_tour=quiz_tour)
    tracks = music_database.get_tracks_by_ids(list(track_id2correct))
    artist_id2artist = music_database.get_artists_by_ids(list({artist_id for track in tracks for artist_id in track.artists}))
    track_id2artists = {track.track_id: [artist_id2artist[artist_id] for artist_id in track.artists] for track in tracks}
    track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=tracks) if settings.show_knowledge_status else {}

    template = templates.get_template("quiz_tours/quiz_tour.html")
    content = template.render(
        user=user,
        page="quiz_tour",
        version=get_static_hash(),
        quiz_tour=quiz_tour,
        statuses=statuses,
        track_id2status=track_id2status,
        tracks=tracks,
        track_id2correct=track_id2correct,
        artist_id2artist=artist_id2artist,
        track_id2artists=track_id2artists,
        track_id2scale=track_id2scale,
        get_word_form=get_word_form,
        jsonable_encoder=jsonable_encoder,
        format_time=format_time
    )
    return HTMLResponse(content=content)


@router.get("/quiz-tours/{quiz_tour_id}")
def get_quiz_tour_question(quiz_tour_id: int, user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return login_redirect(back_url=f"/quiz-tours/{quiz_tour_id}")

    quiz_tour = quiz_tours_database.get_quiz_tour(quiz_tour_id=quiz_tour_id)

    if not quiz_tour:
        return send_error(user=user, title="Запрашиваемый квиз не существует", text="Не удалось найти запрашиваемый квиз. Возможно, он был удалён или ещё не был создан.")

    settings = database.get_settings(username=user.username)
    quiz_tour_question = quiz_tours_database.get_quiz_tour_question(username=user.username, quiz_tour=quiz_tour)

    if quiz_tour_question is None:
        return RedirectResponse(f"/quiz-tour/{quiz_tour_id}")

    question = quiz_tour_question.question
    track = music_database.get_track(track_id=question.track_id)
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=track.artists)
    artist_id2scale = questions_database.get_artists_scales(username=user.username, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}
    track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=[track]) if settings.show_knowledge_status else {}
    artist_id2note = music_database.get_artist_notes(artist_ids=track.artists, username=user.username, with_text=True)
    note = music_database.get_note(artist_id=track.artists[0], username=user.username) if len(track.artists) == 1 else None

    template = templates.get_template("user/question.html")
    content = template.render(
        user=user,
        page="quiz_tour_question",
        version=get_static_hash(),
        settings=settings,
        quiz_tour=quiz_tour,
        question_id=quiz_tour_question.question_id,
        question=question,
        track=track,
        note=note,
        artist_id2note=artist_id2note,
        artist_id2artist=artist_id2artist,
        artist_id2scale=artist_id2scale,
        track_id2scale=track_id2scale,
        jsonable_encoder=jsonable_encoder,
        QuizTourType=QuizTourType,
        get_word_form=get_word_form,
        get_top_letter=get_top_letter,
        get_name_length=get_name_length
    )
    return HTMLResponse(content=content)


@router.post("/quiz-tours")
def search_quiz_tours(params: QuizToursSearch, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    total, quiz_tours = quiz_tours_database.get_quiz_tours(username=user.username if user else None, params=params)
    quiz_tour_id2statuses = quiz_tours_database.get_quiz_tours_statuses(username=user.username, quiz_tours=quiz_tours) if user else {}
    return JSONResponse({"status": "success", "total": total, "quiz_tours": jsonable_encoder(quiz_tours), "statuses": quiz_tour_id2statuses})


@router.post("/answer-quiz-tour-question")
def answer_question(answer: QuizTourQuestionAnswer, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if not quiz_tours_database.have_question(username=user.username, question_id=answer.question_id):
        return JSONResponse({"status": "error", "message": "В базе отсутствует вопрос, на который можно ответить"})

    quiz_tours_database.answer_question(user.username, answer)
    return JSONResponse({"status": "success"})


@router.get("/add-quiz-tour")
def get_add_quiz_tour(user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return login_redirect(back_url="/add-quiz-tour")

    if user.role == UserRole.USER:
        return send_error(title="Доступ запрещён", text="Эта страница доступна только администраторам", user=user)

    template = templates.get_template("quiz_tours/add_quiz_tour.html")
    content = template.render(
        user=user,
        page="add_quiz_tour",
        version=get_static_hash(),
        QuizTourType=QuizTourType
    )
    return HTMLResponse(content=content)


@router.post("/add-quiz-tour")
def add_quiz_tour(params: QuizTourAdd, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    settings = params.to_settings()

    images_dir = os.path.join(os.path.dirname(__file__), "..", "..", "web", "images", "quiz_tours")
    image_name = random.choice(os.listdir(os.path.join(images_dir, params.image_dir)))

    quiz_tour_params = {
        "name": params.name,
        "description": params.description,
        "image_url": f"/images/quiz_tours/{params.image_dir}/{image_name}",
        "tags": params.to_tags()
    }

    quiz_tour = quiz_tours_database.generate_tour(quiz_tour_params, quiz_tour_type=params.mechanics, settings=settings, questions_count=params.questions_count)

    if not quiz_tour:
        return JSONResponse({"status": "error", "message": "не удалось подобрать треки"})

    return JSONResponse({"status": "success"})
