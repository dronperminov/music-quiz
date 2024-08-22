from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from src import logger, music_database, yandex_music_parser
from src.api import templates
from src.entities.user import User
from src.enums import UserRole
from src.query_params.artist_parse import ArtistParse
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
def parse_artist(params: ArtistParse, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    try:
        playlist = yandex_music_parser.parse_playlist(params.artist_id, "yamusic-bestsongs", max_artists=params.max_artists, max_tracks=params.max_tracks)
        if playlist:
            tracks, artists = playlist
        else:
            logger.warning(f'Playlist for "{params.artist_id}" does not exists, try to add artist')
            tracks, artists = yandex_music_parser.parse_artist(params.artist_id, max_artists=params.max_artists, max_tracks=params.max_tracks)

        music_database.add_from_yandex(artists=artists, tracks=tracks, username=user.username)
        return JSONResponse({"status": "success", "tracks": len(tracks), "artists": len(artists)})
    except Exception as error:
        return JSONResponse({"status": "error", "message": str(error)})


@router.post("/parse-chart")
def parse_chart(user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    try:
        tracks, artists = yandex_music_parser.parse_chart(max_tracks=1000, max_artists=4)
        music_database.add_from_yandex(artists=artists, tracks=tracks, username=user.username)
        return JSONResponse({"status": "success", "tracks": len(tracks), "artists": len(artists)})
    except Exception as error:
        return JSONResponse({"status": "error", "message": str(error)})
