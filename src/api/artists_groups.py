from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import music_database
from src.api import templates
from src.entities.user import User
from src.query_params.artists_groups_search import ArtistsGroupsSearch
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/artists-groups")
def get_artists_groups(user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    template = templates.get_template("artists_groups/artists_groups.html")
    content = template.render(
        user=user,
        page="artists_groups",
        version=get_static_hash()
    )
    return HTMLResponse(content=content)


@router.post("/artists-groups")
def search_artist_groups(params: ArtistsGroupsSearch) -> JSONResponse:
    total, artists_groups = music_database.search_artists_groups(params=params)
    artist_id2name = music_database.get_artist_names_by_ids(list({artist_id for group in artists_groups for artist_id in group.artist_ids}))
    return JSONResponse({"status": "success", "total": total, "artists_groups": jsonable_encoder(artists_groups), "artist_id2name": jsonable_encoder(artist_id2name)})
