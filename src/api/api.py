from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
def index() -> JSONResponse:
    return JSONResponse({"status": "OK"})
