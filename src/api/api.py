from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from src import yandex_music_parser

router = APIRouter()


@router.get("/")
def index() -> JSONResponse:
    return JSONResponse({"status": "OK"})


@router.post("/get-direct-link")
def get_direct_link(yandex_id: str = Body(..., embed=True)) -> JSONResponse:
    direct_link = yandex_music_parser.get_track_link(yandex_id)

    if not direct_link:
        return JSONResponse({"status": "error", "message": "Не удалось получить ссылку на аудио"})

    return JSONResponse({"status": "success", "direct_link": direct_link})
