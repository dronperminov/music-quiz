from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, Response

from src import database, music_database, quiz_tours_database, yandex_music_parser
from src.api import login_redirect, send_error, templates
from src.entities.user import User
from src.enums import UserRole
from src.query_params.activity_search import ActivitySearch
from src.query_params.artists_parse import ArtistsParse
from src.query_params.history_query import HistoryQuery
from src.query_params.playlist_parse import PlaylistParse
from src.query_params.top_players_query import TopPlayersQuery
from src.query_params.tracks_parse import TracksParse
from src.utils.auth import get_user
from src.utils.common import get_static_hash, get_word_form

router = APIRouter()


@router.get("/")
def index(user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    top_players = quiz_tours_database.get_top_players(query={})

    template = templates.get_template("index.html")
    content = template.render(
        user=user,
        page="index",
        version=get_static_hash(),
        top_players=top_players,
        get_word_form=get_word_form
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


@router.post("/parse-tracks")
def parse_tracks(params: TracksParse, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    try:
        tracks, artists = yandex_music_parser.parse_tracks(params.track_ids, max_artists=4)
        new_artists, new_tracks = music_database.add_from_yandex(artists=artists, tracks=tracks, username=user.username)
        return JSONResponse({"status": "success", "tracks": len(tracks), "artists": len(artists), "new_tracks": new_tracks, "new_artists": new_artists})
    except Exception as error:
        return JSONResponse({"status": "error", "message": str(error)})


@router.post("/parse-playlist")
def parse_playlist(params: PlaylistParse, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    try:
        tracks, artists = yandex_music_parser.parse_playlist(params.playlist_id, params.playlist_username, max_artists=4, max_tracks=params.max_tracks)
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


@router.get("/activity")
def activity(user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return login_redirect(back_url="/activity")

    if user.role == UserRole.USER:
        return send_error(title="Доступ запрещён", text="Эта страница доступна только администраторам", user=user)

    template = templates.get_template("activity.html")
    content = template.render(user=user, page="activity", version=get_static_hash())
    return HTMLResponse(content=content)


@router.post("/get-activity")
def get_activity(params: ActivitySearch, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    total, activities = database.get_activity(params=params)
    users = database.get_users(usernames=list({action.username for action in activities}))
    username2user = {user.username: {"avatar_url": user.avatar_url, "full_name": user.full_name} for user in users}
    return JSONResponse({"status": "success", "total": total, "activity": jsonable_encoder(activities), "username2user": username2user})
