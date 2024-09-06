import asyncio
from typing import Optional

from fastapi import APIRouter, Body, Cookie, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

from src import database, logger, music_database, questions_database
from src.api import templates
from src.entities.session import Session
from src.entities.user import User
from src.query_params.question_answer import MultiPlayerQuestionAnswer, QuestionAnswer
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

    session = Session.create(session_id=session_id, username=user.username)
    database.sessions.insert_one(session.to_dict())
    return JSONResponse({"status": "success", "session_id": session_id, "username": user.username})


@router.post("/check-multiplayer-session")
async def check_multiplayer_session(session_id: str = Body(..., embed=True), remove_statistics: bool = Body(..., embed=True), user: User = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    session = database.get_session(session_id=session_id)
    if not session:
        return JSONResponse({"status": "error", "message": "Сессия не существует"})

    if session.created_by not in session.players and user.username != session.created_by:
        return JSONResponse({"status": "error", "message": "Автор сессии не подключен"})

    if session.created_by == user.username and remove_statistics:
        session.clear_statistics()
        database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})

    return JSONResponse({"status": "success", "username": user.username})


@router.post("/remove-multiplayer-session")
async def remove_multiplayer_session(session_id: str = Body(..., embed=True), user: User = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    session = database.get_session(session_id=session_id)
    if not session:
        return JSONResponse({"status": "error", "message": "Сессия не существует"})

    if user.username != session.created_by:
        return JSONResponse({"status": "error", "message": "Только создатель сессии может удалить эту сессию"})

    await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "remove"))
    database.sessions.delete_one({"session_id": session.session_id})
    return JSONResponse({"status": "success"})


def get_session_message(session_id: str, username: str, action: str) -> dict:
    message = {
        "session_id": session_id,
        "username": username,
        "action": action
    }

    session = database.get_session(session_id=session_id)
    if not session:
        return message

    users = database.users.find({"username": {"$in": session.players}}, {"username": 1, "avatar_url": 1, "full_name": 1, "_id": 0})
    username2user = {user["username"]: user for user in users}

    message["created_by"] = session.created_by
    message["players"] = [username2user[username] for username in session.players]
    message["answers"] = {username: {"correct": answer.correct, "answer_time": answer.answer_time} for username, answer in session.answers.items()}
    message["question"] = None
    message["statistics"] = {username: [answer.to_dict() for answer in answers] for username, answers in session.statistics.items()}

    if not session.question:
        return message

    settings = database.get_settings(username=username)
    track = music_database.get_track(track_id=session.question.track_id)
    artist_id2artist = music_database.get_artists_by_ids(artist_ids=track.artists)
    artist_id2scale = questions_database.get_artists_scales(username=username, artists=list(artist_id2artist.values())) if settings.show_knowledge_status else {}
    track_id2scale = questions_database.get_tracks_scales(username=username, tracks=[track]) if settings.show_knowledge_status else {}

    message["question"] = jsonable_encoder(session.question)
    message["track"] = jsonable_encoder(track)
    message["artist_id2artist"] = jsonable_encoder(artist_id2artist)
    message["artist_id2scale"] = jsonable_encoder(artist_id2scale)
    message["track_id2scale"] = jsonable_encoder(track_id2scale)
    return message


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

    if user.username not in session.players:
        database.sessions.update_one({"session_id": session_id}, {"$push": {"players": user.username}})

    logger.info(f'@{user.username} connected to the session "{session_id}"')
    await connection_manager.connect(websocket, session_id=session_id)
    asyncio.create_task(connection_manager.ping(websocket, session_id=session_id))
    await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "connect"))

    try:
        while True:
            message = await websocket.receive_text()

            if message == "pong":
                continue

            await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, message))
    except (WebSocketDisconnect, OSError):
        connection_manager.disconnect(websocket, session_id=session_id)
        logger.info(f'@{user.username} disconnected from the session "{session_id}"')

        if database.sessions.find_one({"session_id": session_id}):
            database.sessions.update_one({"session_id": session_id}, {"$pull": {"players": user.username}})  # TODO: подумать, как сделать правильно
            await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "disconnect"))


@router.get("/multi-player")
def multi_player(user: Optional[User] = Depends(get_user)) -> HTMLResponse:
    template = templates.get_template("multi_player/multi_player.html")
    content = template.render(user=user, page="multi_player", version=get_static_hash())
    return HTMLResponse(content=content)


@router.post("/get-multi-player-question")
async def get_multi_player_question(session_id: str = Body(..., embed=True), user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    session = database.get_session(session_id=session_id)
    if not session:
        return JSONResponse({"status": "error", "message": f'Не удалось найти сессию с идентификатором "{session_id}"'})

    settings = database.get_settings(username=session.created_by)
    question = questions_database.get_question(settings)

    if question is None:
        return JSONResponse({"status": "error", "message": "Не удалось сгенерировать вопрос, так как нет треков, удовлетворяющих выбранным настройкам"})

    session.set_question(question)
    database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})
    await connection_manager.broadcast(session_id=session_id, message=get_session_message(session_id, user.username, "question"))
    return JSONResponse({"status": "success"})


@router.post("/answer-multi-player-question")
async def answer_multi_player_question(answer: MultiPlayerQuestionAnswer, user: Optional[User] = Depends(get_user)) -> JSONResponse:
    if not user:
        return JSONResponse({"status": "error", "message": "Пользователь не авторизован"})

    session = database.get_session(session_id=answer.session_id)
    if not session:
        return JSONResponse({"status": "error", "message": f'Не удалось найти сессию с идентификатором "{answer.session_id}"'})

    session.add_answer(username=user.username, answer=QuestionAnswer(correct=answer.correct, answer_time=answer.answer_time))

    if session.all_answered():
        question = session.question

        for username, answer in session.answers.items():
            question.username = username
            question.set_answer(answer)
            database.questions.update_one({"username": username, "correct": None, "group_id": None}, {"$set": question.to_dict()}, upsert=True)

        session.question = None

    database.sessions.update_one({"session_id": session.session_id}, {"$set": session.to_dict()})
    await connection_manager.broadcast(session_id=session.session_id, message=get_session_message(session.session_id, user.username, "answer"))
    return JSONResponse({"status": "success"})
