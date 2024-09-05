from typing import Optional

from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from src import database, music_database, questions_database
from src.api import send_error, templates
from src.entities.user import User
from src.enums import UserRole
from src.query_params.artists_groups_search import ArtistsGroupsSearch
from src.utils.auth import get_user
from src.utils.common import get_static_hash, get_word_form
from src.utils.date_utils import parse_dates

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


@router.get("/artists-groups/{group_id}")
def get_artists_group(group_id: int, username: str = Query(""), period: str = Query(""), user: Optional[User] = Depends(get_user)) -> Response:
    show_user = database.get_user(username=username)
    if username and (not user or username.lower() == user.username.lower() or not show_user):
        return RedirectResponse(url=f"/artists-groups/{group_id}?period={period}")

    if not show_user:
        show_user = user

    artists_group = music_database.get_artists_group(group_id=group_id)

    if artists_group is None:
        return send_error(title="Группа не найдена", text="Не удалось найти запрашиваемую группу схожих исполнителей. Возможно, она был удалена.", user=user)

    artist_id2artists = music_database.get_artists_by_ids(artist_ids=artists_group.artist_ids)
    period = parse_dates(period)
    group_analytics = questions_database.get_group_analytics(username=show_user.username, group=artists_group, period=period) if user else None

    template = templates.get_template("artists_groups/artists_group.html")
    content = template.render(
        user=user,
        page="artists_group",
        version=get_static_hash(),
        artists_group=artists_group,
        show_user=show_user,
        artist_id2artists=artist_id2artists,
        group_analytics=group_analytics,
        get_word_form=get_word_form,
        period=period
    )

    return HTMLResponse(content=content)


@router.post("/artists-groups")
def search_artist_groups(params: ArtistsGroupsSearch, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    total, artists_groups = music_database.search_artists_groups(params=params)
    artist_id2name = music_database.get_artist_names_by_ids(list({artist_id for group in artists_groups for artist_id in group.artist_ids}))
    group_id2tracks_count = music_database.get_groups_tracks_count(groups=artists_groups)

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
        "group_id2scale": jsonable_encoder(group_id2scale),
        "group_id2tracks_count": jsonable_encoder(group_id2tracks_count)
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
