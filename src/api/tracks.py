from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import database, music_database, questions_database
from src.api import templates
from src.entities.user import User
from src.enums import ArtistType, ArtistsCount, Genre, Language, UserRole
from src.query_params.artist_update import ArtistUpdate
from src.query_params.artists_search import ArtistsSearch
from src.query_params.artists_search_query import ArtistsSearchQuery
from src.query_params.track_update import TrackUpdate
from src.utils.auth import get_user
from src.utils.common import get_static_hash, get_word_form

router = APIRouter()


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

    music_database.update_track(track_id=params.track_id, diff=track.get_diff(params.to_data()), username=user.username)
    return JSONResponse({"status": "success"})
