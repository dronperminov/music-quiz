from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src import database, music_database
from src.entities.user import User
from src.enums import UserRole
from src.query_params.track_update import TrackUpdate
from src.utils.auth import get_user

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
