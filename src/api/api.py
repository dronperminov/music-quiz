from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from src import logger, music_database, yandex_music_parser
from src.api import templates
from src.entities.user import User
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/")
def index(user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    template = templates.get_template("index.html")
    content = template.render(
        user=user,
        page="index",
        version=get_static_hash()
    )

    return HTMLResponse(content=content)


@router.post("/get-direct-link")
def get_direct_link(yandex_id: str = Body(..., embed=True)) -> JSONResponse:
    direct_link = yandex_music_parser.get_track_link(yandex_id)

    if not direct_link:
        return JSONResponse({"status": "error", "message": "Не удалось получить ссылку на аудио"})

    return JSONResponse({"status": "success", "direct_link": direct_link})


@router.post("/parse-artist")
def parse_artist(artist_id: int = Body(..., embed=True), user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    try:
        playlist = yandex_music_parser.parse_playlist(playlist_username="yamusic-bestsongs", playlist_id=artist_id, max_artists=4, max_tracks=20)
        if playlist:
            tracks, artists = playlist
        else:
            logger.warning(f'Playlist for "{artist_id}" does not exists, try to add artist')
            tracks, artists = yandex_music_parser.parse_artist(artist_id=artist_id, max_artists=4, max_tracks=20)

        music_database.add_from_yandex(artists=artists, tracks=tracks, username=user.username)
        return JSONResponse({"status": "success", "tracks": len(tracks), "artists": len(artists)})
    except Exception as error:
        return JSONResponse({"status": "error", "message": str(error)})
