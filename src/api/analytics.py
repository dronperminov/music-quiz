import urllib.parse
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src import database, music_database, questions_database, quiz_tours_database
from src.api import templates
from src.entities.user import User
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/analytics")
def get_analytics(username: str = Query(""), user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return RedirectResponse(url=f'/login?back_url={urllib.parse.quote("/analytics", safe="")}')

    show_user = database.get_user(username=username)
    if username and (username.lower() == user.username.lower() or not show_user):
        return RedirectResponse(url="/analytics")

    if not show_user:
        show_user = user

    analytics = questions_database.get_analytics(username=show_user.username)
    rating = quiz_tours_database.get_rating(username=show_user.username, query={})
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=analytics.artists.get_artist_ids())

    template = templates.get_template("user/analytics.html")
    content = template.render(
        user=user,
        page="analytics",
        version=get_static_hash(),
        analytics=analytics,
        rating=rating[0] if rating else 0,
        artist_id2artist=artist_id2artist,
        show_user=show_user
    )
    return HTMLResponse(content=content)
