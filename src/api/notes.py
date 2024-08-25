from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src import music_database
from src.entities.user import User
from src.query_params.note_update import NoteUpdate
from src.utils.auth import get_user

router = APIRouter()


@router.post("/update-note")
def update_note(params: NoteUpdate, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    artist = music_database.get_artist(artist_id=params.artist_id)
    if artist is None:
        return JSONResponse({"status": "error", "message": f"Не удалось найти исполнителя с artist_id = {params.artist_id} в базе"})

    note = music_database.get_note(artist_id=params.artist_id, username=user.username)
    if note is None:
        music_database.add_note(params.to_note(username=user.username))
    else:
        if params.text is not None:
            note.text = params.text

        if params.track is not None:
            note.update_track(track_id=params.track.track_id, seek=params.track.seek)

        music_database.update_note(note)

    return JSONResponse({"status": "success"})
