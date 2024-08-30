from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import database, music_database, quiz_tours_database, yandex_music_parser
from src.api import templates
from src.entities.user import User
from src.enums import UserRole
from src.query_params.artists_parse import ArtistsParse
from src.query_params.history_query import HistoryQuery
from src.query_params.top_players_query import TopPlayersQuery
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/")
def index(user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    top_players = quiz_tours_database.get_top_players(query={})

    template = templates.get_template("index.html")
    content = template.render(
        user=user,
        page="index",
        version=get_static_hash(),
        top_players=top_players
    )

    return HTMLResponse(content=content)


@router.post("/get-direct-link")
def get_direct_link(yandex_id: str = Body(..., embed=True)) -> JSONResponse:
    direct_link = yandex_music_parser.get_track_link(yandex_id)

    if not direct_link:
        return JSONResponse({"status": "error", "message": "Не удалось получить ссылку на аудио"})

    return JSONResponse({"status": "success", "direct_link": direct_link})


@router.post("/parse-artists")
def parse_artists(params: ArtistsParse, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    try:
        tracks, artists = yandex_music_parser.parse_artists(params.artist_ids, params.max_tracks, params.max_artists, params.from_playlist)
        new_artists, new_tracks = music_database.add_from_yandex(artists=artists, tracks=tracks, username=user.username)
        return JSONResponse({"status": "success", "tracks": len(tracks), "artists": len(artists), "new_tracks": new_tracks, "new_artists": new_artists})
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
        new_artists, new_tracks = music_database.add_from_yandex(artists=artists, tracks=tracks, username=user.username)
        return JSONResponse({"status": "success", "tracks": len(tracks), "artists": len(artists), "new_tracks": new_tracks, "new_artists": new_artists})
    except Exception as error:
        return JSONResponse({"status": "error", "message": str(error)})


@router.post("/history")
def get_history(params: HistoryQuery) -> JSONResponse:
    query = {"name": {"$in": params.actions}}
    history = list(database.history.find(query, {"_id": 0}).sort("timestamp", -1).skip(params.skip).limit(params.limit))
    return JSONResponse({"status": "success", "history": jsonable_encoder(history)})


@router.post("/get-top-players")
def get_top_players(params: TopPlayersQuery) -> JSONResponse:
    players = quiz_tours_database.get_top_players(params.to_query())
    return JSONResponse({"status": "success", "players": jsonable_encoder(players)})
