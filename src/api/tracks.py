import random
import urllib.parse
from typing import Optional

from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import database, music_database, questions_database
from src.api import send_error, templates
from src.entities.user import User
from src.enums import UserRole
from src.query_params.track_update import TrackUpdate
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/tracks/{track_id}")
def get_track(track_id: int, seek: float = Query(0), as_unknown: bool = Query(False), user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    track = music_database.get_track(track_id=track_id)

    if not track:
        return send_error(title="Трек не найден", text="Не удалось найти запрашиваемый трек. Возможно, он был удалён", user=user)

    artist_id2artist = music_database.get_artists_by_ids(artist_ids=track.artists)

    if user:
        settings = database.get_settings(username=user.username)
        track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=[track]) if settings.show_knowledge_status else {}
        artist_id2scale = questions_database.get_artists_scales(username=user.username, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}
    else:
        settings = None
        track_id2scale = {}
        artist_id2scale = {}

    template = templates.get_template("tracks/track.html")
    content = template.render(
        user=user,
        page="track",
        version=get_static_hash(),
        settings=settings,
        track=track,
        seek=seek,
        as_unknown=as_unknown,
        artist_id2artist=artist_id2artist,
        track_id2scale=track_id2scale,
        artist_id2scale=artist_id2scale,
        jsonable_encoder=jsonable_encoder
    )
    return HTMLResponse(content=content)


@router.get("/markup-track")
def get_markup(track_id: int = Query(0), language: str = Query(""), user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        back_url = urllib.parse.quote(f"/markup-track?track_id={track_id}", safe="")
        return RedirectResponse(url=f"/login?back_url={back_url}")

    if track_id == 0:
        query = {"lyrics": {"$ne": None}, "lyrics.lrc": True, "lyrics.validated": False, "artists.1": {"$exists": False}}
        if language != "":
            query["language"] = language

        track_id = random.choice([track["track_id"] for track in database.tracks.find(query, {"track_id": 1})])

    track = music_database.get_track(track_id=track_id)

    if not track:
        return send_error(title="Трек не найден", text="Не удалось найти запрашиваемый трек. Возможно, он был удалён", user=user)

    artist_id2name = music_database.get_artist_names_by_ids(artist_ids=track.artists)
    settings = database.get_settings(username=user.username)

    template = templates.get_template("tracks/markup.html")
    content = template.render(
        user=user,
        page="markup-track",
        version=get_static_hash(),
        settings=settings,
        track=track,
        artist_id2name=artist_id2name,
        jsonable_encoder=jsonable_encoder
    )
    return HTMLResponse(content=content)


@router.get("/track-history/{track_id}")
def get_track_history(track_id: int) -> JSONResponse:
    history = list(database.history.find({"track_id": track_id}, {"_id": 0}).sort("timestamp", -1))
    return JSONResponse({"status": "success", "history": jsonable_encoder(history)})


@router.post("/update-track")
def update_track(params: TrackUpdate, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    track = music_database.get_track(track_id=params.track_id)
    if track is None:
        return JSONResponse({"status": "error", "message": f"Не удалось найти трек с track_id = {params.track_id} в базе"})

    music_database.update_track(track_id=params.track_id, diff=track.get_diff(params.to_data(track.lyrics)), username=user.username)
    return JSONResponse({"status": "success"})


@router.post("/remove-track")
def remove_track(track_id: int = Body(..., embed=True), user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role != UserRole.OWNER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    track = music_database.get_track(track_id=track_id)
    if track is None:
        return JSONResponse({"status": "error", "message": f"Не удалось найти трек с track_id = {track_id} в базе"})

    music_database.remove_track(track_id=track_id, username=user.username)
    return JSONResponse({"status": "success"})
