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
from src.utils.auth import get_user
from src.utils.common import get_static_hash, get_word_form

router = APIRouter()


@router.get("/artists")
def get_artists(user: Optional[User] = Depends(get_user), params: ArtistsSearchQuery = Depends()) -> HTMLResponse:
    search_params = params.to_search_params(user is not None)
    last_added_artists = music_database.get_last_artists(order_field="metadata.created_at", order_type=-1, count=10)
    last_updated_artists = music_database.get_last_artists(order_field="metadata.updated_at", order_type=-1, count=10)
    top_listened_artists = music_database.get_last_artists(order_field="listen_count", order_type=-1, count=10)
    guessed_artists = music_database.get_last_artists(order_field="name_lowercase", order_type=1, target="questions", username=user.username, count=10) if user else []

    template = templates.get_template("artists/artists.html")
    content = template.render(
        user=user,
        page="artists",
        version=get_static_hash(),
        artists_count=music_database.get_artists_count(),
        tracks_count=music_database.get_tracks_count(),
        last_added_artists=last_added_artists,
        last_updated_artists=last_updated_artists,
        top_listened_artists=top_listened_artists,
        guessed_artists=guessed_artists,
        get_word_form=get_word_form,
        Genre=Genre,
        ArtistType=ArtistType,
        ArtistsCount=ArtistsCount,
        Language=Language,
        search_params=search_params
    )
    return HTMLResponse(content=content)


@router.post("/artists")
def search_artists(params: ArtistsSearch, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    total, artists = music_database.search_artists(params=params, username=user.username if user else None)

    if user:
        settings = database.get_settings(username=user.username)
        artist_id2scale = questions_database.get_artists_scales(username=user.username, artists=artists) if settings.show_knowledge_status else {}
    else:
        artist_id2scale = {}

    return JSONResponse({"status": "success", "total": total, "artists": jsonable_encoder(artists), "artist_id2scale": artist_id2scale})


@router.get("/artists/{artist_id}")
def get_artist(artist_id: int, user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    artist = music_database.get_artist(artist_id=artist_id)
    tracks = sorted(music_database.get_artist_tracks(artist_id), key=lambda track: artist.tracks[track.track_id])
    artist2name = music_database.get_artist_names(tracks)

    if user:
        settings = database.get_settings(username=user.username)
        track_id2scale = questions_database.get_tracks_scales(username=user.username, tracks=tracks) if settings.show_knowledge_status else {}
    else:
        track_id2scale = {}

    template = templates.get_template("artists/artist.html")
    content = template.render(
        user=user,
        page="artist",
        version=get_static_hash(),
        artist=artist,
        tracks=tracks,
        artist2name=artist2name,
        track_id2scale=track_id2scale,
        get_word_form=get_word_form,
        jsonable_encoder=jsonable_encoder
    )
    return HTMLResponse(content=content)


@router.get("/artist-history/{artist_id}")
def get_artist_history(artist_id: int) -> JSONResponse:
    history = list(database.history.find({"artist_id": artist_id}, {"_id": 0}).sort("timestamp", -1))
    return JSONResponse({"status": "success", "history": jsonable_encoder(history)})


@router.post("/update-artist")
def update_artist(params: ArtistUpdate, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role == UserRole.USER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    artist = music_database.get_artist(artist_id=params.artist_id)
    if artist is None:
        return JSONResponse({"status": "error", "message": f"Не удалось найти исполнителя с artist_id = {params.artist_id} в базе"})

    music_database.update_artist(artist_id=params.artist_id, diff=artist.get_diff(params.to_data()), username=user.username)
    return JSONResponse({"status": "success"})
