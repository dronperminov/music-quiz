import urllib.parse
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import database, music_database, questions_database
from src.api import send_error, templates
from src.entities.user import User
from src.query_params.question_answer import QuestionAnswer
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/question")
def get_question(user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return RedirectResponse(url=f'/login?back_url={urllib.parse.quote("/question", safe="")}')

    settings = database.get_settings(username=user.username)
    question = questions_database.get_question(settings)

    if question is None:
        return send_error(user=user, title="Не удалось сгенерировать вопрос", text='Нет треков, удовлетворяющих выбранным <a class="link" href="/settings">настройкам</a>.')

    track = music_database.get_track(track_id=question.track_id)
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=track.artists)
    artist_id2scale = questions_database.get_artists_scales(username=user.username, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}
    track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=[track]) if settings.show_knowledge_status else {}
    artist_id2note = music_database.get_artist_notes(artist_ids=track.artists, username=user.username, with_text=True)
    note = music_database.get_note(artist_id=track.artists[0], username=user.username) if len(track.artists) == 1 else None

    template = templates.get_template("user/question.html")
    content = template.render(
        user=user,
        page="question",
        version=get_static_hash(),
        settings=settings,
        question=question,
        track=track,
        note=note,
        artist_id2note=artist_id2note,
        artist_id2artist=artist_id2artist,
        artist_id2scale=artist_id2scale,
        track_id2scale=track_id2scale,
        jsonable_encoder=jsonable_encoder
    )
    return HTMLResponse(content=content)


@router.get("/group-question/{group_id}")
def get_group_question(group_id: int, user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return RedirectResponse(url=f'/login?back_url={urllib.parse.quote(f"/question?group_id={group_id}", safe="")}')

    group = music_database.get_artists_group(group_id=group_id)

    if not group:
        return send_error(user=user, title="Запрашиваемая группа не существует", text="Не удалось найти заданную группу, возможно, она была удалена или ещё не была создана.")

    if not group.artist_ids:
        return send_error(user=user, title=f'Группа "{group.name}" пустая', text="В этой группе пока нет исполнителей.")

    settings = database.get_settings(username=user.username)
    question = questions_database.get_question(settings, group_id=group_id)

    if question is None:
        return send_error(user=user, title=f'Не удалось сгенерировать вопрос для группы "{group.name}"', text="Кажется, у исполнителей этой группы закончились треки.")

    track = music_database.get_track(track_id=question.track_id)
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=track.artists + group.artist_ids)
    artist_id2scale = questions_database.get_artists_scales(username=user.username, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}
    track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=[track]) if settings.show_knowledge_status else {}
    artist_id2note = music_database.get_artist_notes(artist_ids=track.artists, username=user.username, with_text=True)
    note = music_database.get_note(artist_id=track.artists[0], username=user.username) if len(track.artists) == 1 else None

    template = templates.get_template("user/question.html")
    content = template.render(
        user=user,
        page="question",
        version=get_static_hash(),
        settings=settings,
        question=question,
        track=track,
        note=note,
        artist_id2note=artist_id2note,
        artist_id2artist=artist_id2artist,
        group=group,
        group_variants=group.get_variants(track, settings.artists_group_settings.max_variants),
        artist_id2scale=artist_id2scale,
        track_id2scale=track_id2scale,
        jsonable_encoder=jsonable_encoder
    )
    return HTMLResponse(content=content)


@router.post("/answer-question")
def answer_question(answer: QuestionAnswer, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if not questions_database.have_question(user.username, group_id=answer.group_id):
        return JSONResponse({"status": "error", "message": "В базе отсутствует вопрос, на который можно ответить"})

    questions_database.answer_question(user.username, answer)
    return JSONResponse({"status": "success"})
