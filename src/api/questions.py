import urllib.parse
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src import database, music_database, questions_database
from src.api import templates
from src.entities.user import User
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/question")
def get_question(user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return RedirectResponse(url=f'/login?back_url={urllib.parse.quote("/question", safe="")}')

    settings = database.get_settings(username=user.username)
    question = questions_database.generate_question(settings)
    track = music_database.get_track(track_id=question.track_id)
    artist_id2artist = music_database.get_track_artists(track=track)

    template = templates.get_template("user/question.html")
    content = template.render(
        user=user,
        page="question",
        version=get_static_hash(),
        settings=settings,
        question=question,
        track=track,
        artist_id2artist=artist_id2artist,
        jsonable_encoder=jsonable_encoder
    )
    return HTMLResponse(content=content)
