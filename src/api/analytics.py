import urllib.parse
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from src import music_database, questions_database
from src.api import templates
from src.entities.user import User
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/analytics")
def get_analytics(user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return RedirectResponse(url=f'/login?back_url={urllib.parse.quote("/analytics", safe="")}')

    analytics = questions_database.get_analytics(username=user.username)
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=analytics.artists.get_artist_ids())

    template = templates.get_template("user/analytics.html")
    content = template.render(
        user=user,
        page="analytics",
        version=get_static_hash(),
        analytics=analytics,
        artist_id2artist=artist_id2artist
    )
    return HTMLResponse(content=content)
