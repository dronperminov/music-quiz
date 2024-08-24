from typing import Optional

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import database, music_database, questions_database
from src.api import templates
from src.entities.user import User
from src.enums import UserRole
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


@router.post("/remove-artists-group")
def remove_artists_group(group_id: int = Body(..., embed=True), user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if user.role != UserRole.OWNER:
        return JSONResponse({"status": "error", "message": "Пользователь не является администратором"})

    group = music_database.get_artists_group(group_id=group_id)
    if group is None:
        return JSONResponse({"status": "error", "message": f"Не удалось найти группу с group_id = {group_id} в базе"})

    music_database.remove_artists_group(group_id=group_id, username=user.username)
    return JSONResponse({"status": "success"})


@router.get("/artists-group-history/{group_id}")
def get_artists_group_history(group_id: int) -> JSONResponse:
    history = list(database.history.find({"$or": [{"group_id": group_id}, {"group.group_id": group_id}]}, {"_id": 0}).sort("timestamp", -1))
    return JSONResponse({"status": "success", "history": jsonable_encoder(history)})
