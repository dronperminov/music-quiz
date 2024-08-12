from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from src import music_database
from src.api import templates
from src.utils.common import get_static_hash, get_word_form

router = APIRouter()


@router.get("/artists")
def get_artists() -> HTMLResponse:
    artists = music_database.get_artists()

    template = templates.get_template("artists/artists.html")
    content = template.render(
        page="artists",
        version=get_static_hash(),
        artists=artists,
        get_word_form=get_word_form
    )
    return HTMLResponse(content=content)
