from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, Response

from src import database, music_database, questions_database
from src.api import login_redirect, templates
from src.entities.user import User
from src.query_params.note_update import NoteUpdate
from src.query_params.notes_search import NotesSearch, NotesSearchQuery
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/notes")
def get_notes(params: NotesSearchQuery = Depends(), user: Optional[User] = Depends(get_user)) -> Response:
    if not user:
        return login_redirect(back_url="/notes")

    settings = database.get_settings(username=user.username)
    template = templates.get_template("user/notes.html")
    content = template.render(
        user=user,
        page="notes",
        version=get_static_hash(),
        settings=settings,
        search_params=params.to_params()
    )
    return HTMLResponse(content=content)


@router.post("/notes")
def search_notes(params: NotesSearch, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    total, notes = music_database.get_user_notes(username=user.username, params=params)

    settings = database.get_settings(username=user.username)
    tracks = music_database.get_tracks_by_ids(track_ids=[track_id for note in notes for track_id in note.track_id2seek])
    track_id2track = {track.track_id: track for track in tracks}
    track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=tracks) if settings.show_knowledge_status else {}

    artist_ids = list({note.artist_id for note in notes}.union({artist_id for track in tracks for artist_id in track.artists}))
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=artist_ids)
    artist_id2scale = questions_database.get_artists_scales(username=user.username, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}

    return JSONResponse({
        "status": "success",
        "total": total,
        "notes": jsonable_encoder(notes),
        "artist_id2artist": jsonable_encoder(artist_id2artist),
        "artist_id2scale": jsonable_encoder(artist_id2scale),
        "track_id2track": jsonable_encoder(track_id2track),
        "track_id2scale": jsonable_encoder(track_id2scale)
    })


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
