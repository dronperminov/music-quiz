import asyncio
import json
import re
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, Cookie, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.websockets import WebSocket, WebSocketDisconnect

from src import database, logger, music_database, questions_database
from src.api import login_redirect, templates
from src.entities.question_settings import QuestionSettings
from src.entities.session import Session
from src.entities.settings import Settings
from src.entities.user import User
from src.enums import ArtistsCount, Genre, Language, QuestionType
from src.query_params.question_answer import QuestionAnswer
from src.utils.auth import get_user, token_to_user
from src.utils.common import get_static_hash
from src.utils.connection_manager import ConnectionManager

router = APIRouter()
connection_manager = ConnectionManager(logger=logger)


@router.post("/create-multiplayer-session")
async def create_multiplayer_session(session_id: str = Body(..., embed=True), user: User = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    if database.get_session(session_id=session_id):
        return JSONResponse({"status": "error", "message": f'Сессия с идентификатором "{session_id}" уже есть'})

    session = Session.create(session_id=session_id, username=user.username, question_settings=QuestionSettings.default())
    database.sessions.insert_one(session.to_dict())
    return JSONResponse({"status": "success", "session_id": session_id, "username": user.username})


@router.post("/check-multiplayer-session")
async def check_multiplayer_session(session_id: str = Body(..., embed=True), remove_statistics: bool = Body(..., embed=True), user: User = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    session = database.get_session(session_id=session_id)
    if not session:
        return JSONResponse({"status": "error", "message": "Сессия не существует"})

    if session.created_by == user.username and remove_statistics:
        session.clear_statistics()
        database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})

    return JSONResponse({"status": "success", "username": user.username})


def get_session_message(session_id: str, username: str, action: str) -> dict:
    message = {
        "session_id": session_id,
        "username": username,
        "action": action
    }

    session = database.get_session(session_id=session_id)
    if not session:
        return message

    users = database.get_users(usernames=session.players)
    username2user = {user.username: {"username": user.username, "avatar_url": user.avatar_url, "full_name": user.full_name} for user in users}

    message["created_by"] = session.created_by
    message["players"] = [username2user[username] for username in session.players]
    message["answers"] = {username: {"correct": answer.correct, "answer_time": answer.answer_time} for username, answer in session.answers.items()}
    message["question"] = None
    message["statistics"] = {username: [answer.to_dict() for answer in answers] for username, answers in session.statistics.items()}
    message["question_settings"] = session.question_settings.to_dict()

    if not session.question:
        return message

    track = music_database.get_track(track_id=session.question.track_id)
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=track.artists)

    artist_id2scale = {}
    track_id2scale = {}

    for player in session.players:
        settings = database.get_settings(username=player)
        artist_id2scale[player] = questions_database.get_artists_scales(username=player, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}
        track_id2scale[player] = questions_database.get_tracks_scales(username=player, tracks=[track]) if settings.show_knowledge_status else {}

    message["question"] = jsonable_encoder(session.question)
    message["track"] = jsonable_encoder(track)
    message["artist_id2artist"] = jsonable_encoder(artist_id2artist)
    message["artist_id2scale"] = jsonable_encoder(artist_id2scale)
    message["track_id2scale"] = jsonable_encoder(track_id2scale)
    return message


async def get_session_question(session_id: str, username: str) -> None:
    session = database.get_session(session_id=session_id)
    if not session:
        return

    settings = Settings.default(username="")
    settings.update_question(session.question_settings)
    question = questions_database.get_question(settings, external_questions=session.get_questions())
    session.set_question(question)
    database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})
    await connection_manager.broadcast(session_id=session.session_id, message=get_session_message(session.session_id, username, "question"))


async def check_all_answered(session_id: str, username: str) -> None:
    session = database.get_session(session_id=session_id)

    if not session or session.question is None or len(session.players) < 2 or not session.all_answered():
        return

    question = session.question
    answers = []

    for player, answer in session.answers.items():
        answers.append(answer.correct)

        question.username = player
        question.set_answer(answer)
        database.questions.insert_one(question.to_dict())

    question.username = ""
    question.set_answer(QuestionAnswer(correct=sum(answers) > len(answers) * 0.4, answer_time=None))
    session.add_question(question)
    database.sessions.update_one({"session_id": session_id}, {"$set": session.to_dict()})

    await get_session_question(session_id=session_id, username=username)


async def handle_player_answer(session_id: str, username: str, answer: QuestionAnswer) -> None:
    session = database.get_session(session_id=session_id)
    if not session:
        return

    session.add_answer(username=username, answer=answer)
    database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})
    await connection_manager.broadcast(session_id=session.session_id, message=get_session_message(session.session_id, username, "answer"))
    await check_all_answered(session_id=session_id, username=username)


async def update_settings(session_id: str, settings: dict, username: str) -> None:
    session = database.get_session(session_id=session_id)

    if not session:
        return

    question_settings = QuestionSettings.from_dict(settings)
    if session.update_settings(question_settings=question_settings):
        database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})
        await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, username, "settings"))


@router.websocket("/ws/{session_id}")
async def handle_websocket(websocket: WebSocket, session_id: str, quiz_token: str = Cookie(None)) -> None:
    user = await token_to_user(quiz_token)

    if not user:
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = database.get_session(session_id=session_id)
    if not session:
        await websocket.close(code=1003)
        raise HTTPException(status_code=404, detail="Session not found")

    session.add_player(user.username)
    database.sessions.update_one({"session_id": session_id}, {"$set": session.to_dict()})

    if len(session.players) > 1:
        if session.question is None:
            await get_session_question(session_id=session_id, username=user.username)
        else:
            await check_all_answered(session_id=session_id, username=user.username)

    logger.info(f'@{user.username} connected to the session "{session_id}"')
    await connection_manager.connect(websocket, session_id=session_id)
    asyncio.create_task(connection_manager.ping(websocket, session_id=session_id))
    await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "connect"))

    try:
        while True:
            message = await websocket.receive_text()

            if message == "pong":
                continue

            message = json.loads(message)
            session = database.get_session(session_id=session_id)

            if message["action"] == "answer":
                await handle_player_answer(session_id=session_id, username=user.username, answer=QuestionAnswer.from_dict(message))
            elif message["action"] == "settings":
                await update_settings(session_id=session_id, settings=message["settings"], username=user.username)
            elif message["action"] == "message":
                await connection_manager.broadcast(session_id=session_id, message={"action": "message", "username": user.username, "text": message["text"]})
            elif message["action"] == "reaction":
                await connection_manager.broadcast(session_id=session_id, message={"action": "reaction", "username": user.username, "reaction": message["reaction"]})
            elif message["action"] == "remove" and message["username"] == session.created_by:
                await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "remove"))
                database.sessions.delete_one({"session_id": session_id})
                await websocket.close()
    except (WebSocketDisconnect, OSError, RuntimeError):
        connection_manager.disconnect(websocket, session_id=session_id)
        logger.info(f'@{user.username} disconnected from the session "{session_id}"')

        if session := database.get_session(session_id=session_id):
            session.remove_player(user.username)
            database.sessions.update_one({"session_id": session_id}, {"$set": session.to_dict()})

        await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "disconnect"))
        await check_all_answered(session_id=session_id, username="")


@router.get("/multi-player")
def multi_player(session_id: str = Query(""), user: Optional[User] = Depends(get_user)) -> Response:
    if not re.fullmatch(r"[a-zA-Z\d_\-]+", session_id):
        session_id = ""

    if not user:
        return login_redirect(back_url=f"/multi-player?session_id={session_id}")

    template = templates.get_template("multi_player/multi_player.html")
    settings = database.get_settings(username=user.username)
    content = template.render(
        user=user,
        page="multi_player",
        version=get_static_hash(),
        question_settings=settings.question_settings,
        Genre=Genre,
        Language=Language,
        ArtistsCount=ArtistsCount,
        QuestionType=QuestionType,
        today=datetime.now(),
        session_id=session_id
    )
    return HTMLResponse(content=content)
