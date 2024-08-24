from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import database, music_database, questions_database
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
def search_artist_groups(params: ArtistsGroupsSearch, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    total, artists_groups = music_database.search_artists_groups(params=params)
    artist_id2name = music_database.get_artist_names_by_ids(list({artist_id for group in artists_groups for artist_id in group.artist_ids}))

    if user:
        settings = database.get_settings(username=user.username)
        group_id2scale = questions_database.get_groups_scales(username=user.username, groups=artists_groups) if settings.show_knowledge_status else {}
    else:
        group_id2scale = {}

    return JSONResponse({
        "status": "success",
        "total": total,
        "artists_groups": jsonable_encoder(artists_groups),
        "artist_id2name": jsonable_encoder(artist_id2name),
        "group_id2scale": jsonable_encoder(group_id2scale)
    })
