from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import music_database
from src.api import templates
from src.query_params.artists_search import ArtistsSearch
from src.utils.common import get_static_hash, get_word_form

router = APIRouter()


@router.get("/artists")
def get_artists() -> HTMLResponse:
    last_added_artists = music_database.get_last_added_artists(count=10)
    top_listened_artists = music_database.get_top_listened_artists(count=10)

    template = templates.get_template("artists/artists.html")
    content = template.render(
        page="artists",
        version=get_static_hash(),
        artists_count=music_database.get_artists_count(),
        last_added_artists=last_added_artists,
        top_listened_artists=top_listened_artists,
        get_word_form=get_word_form
    )
    return HTMLResponse(content=content)


@router.post("/artists")
def search_artists(params: ArtistsSearch) -> JSONResponse:
    artists = music_database.search_artists(params=params)
    return JSONResponse({"status": "success", "artists": jsonable_encoder(artists)})


@router.get("/artists/{artist_id}")
def get_artist(artist_id: int) -> HTMLResponse:
    artist = music_database.get_artist(artist_id=artist_id)
    tracks = sorted(music_database.get_artist_tracks(artist_id), key=lambda track: artist.tracks[track.track_id])
    artist2name = music_database.get_artist_names(tracks)

    template = templates.get_template("artists/artist.html")
    content = template.render(
        page="artist",
        version=get_static_hash(),
        artist=artist,
        tracks=tracks,
        artist2name=artist2name,
        get_word_form=get_word_form
    )
    return HTMLResponse(content=content)
