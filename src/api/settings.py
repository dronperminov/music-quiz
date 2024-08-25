import urllib.parse
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import database
from src.api import templates
from src.entities.artists_group_settings import ArtistsGroupSettings
from src.entities.question_settings import QuestionSettings
from src.entities.user import User
from src.enums import ArtistsCount, Genre, Language, QuestionType
from src.query_params.main_settings import MainSettings
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/settings")
def get_settings(user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return RedirectResponse(url=f'/login?back_url={urllib.parse.quote("/settings", safe="")}')

    settings = database.get_settings(username=user.username)
    template = templates.get_template("user/settings.html")
    content = template.render(
        user=user,
        page="settings",
        version=get_static_hash(),
        settings=settings,
        Genre=Genre,
        Language=Language,
        ArtistsCount=ArtistsCount,
        QuestionType=QuestionType,
        today=datetime.today()
    )
    return HTMLResponse(content=content)


@router.post("/main_settings")
def update_main_settings(main_settings: MainSettings, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    settings = database.get_settings(username=user.username)
    database.update_settings(settings.update_main(main_settings))
    return JSONResponse({"status": "success"})


@router.post("/question_settings")
def update_question_settings(question_settings: QuestionSettings, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    settings = database.get_settings(username=user.username)
    database.update_settings(settings.update_question(question_settings))
    return JSONResponse({"status": "success"})


@router.post("/artists_group_settings")
def update_artists_group_settings(artists_group_settings: ArtistsGroupSettings, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    settings = database.get_settings(username=user.username)
    database.update_settings(settings.update_artists_group(artists_group_settings))
    return JSONResponse({"status": "success"})
