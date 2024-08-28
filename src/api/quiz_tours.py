from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

from src import quiz_tours_database
from src.api import templates
from src.entities.user import User
from src.utils.auth import get_user
from src.utils.common import get_static_hash

router = APIRouter()


@router.get("/quiz-tours")
def get_quiz_tours(user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    template = templates.get_template("quiz_tours/quiz_tours.html")
    content = template.render(
        user=user,
        page="quiz_tours",
        version=get_static_hash()
    )
    return HTMLResponse(content=content)


@router.post("/quiz-tours")
def search_quiz_tours() -> JSONResponse:
    quiz_tours = quiz_tours_database.get_quiz_tours()
    return JSONResponse({"status": "success", "quiz_tours": jsonable_encoder(quiz_tours)})
