import json
from typing import Dict, List

from fastapi.websockets import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str) -> None:
        await websocket.accept()

        if session_id not in self.active_connections:
            self.active_connections[session_id] = []

        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str) -> None:
        self.active_connections[session_id].remove(websocket)

        if not self.active_connections[session_id]:
            del self.active_connections[session_id]

    async def broadcast(self, session_id: str, message: dict) -> None:
        if session_id not in self.active_connections:
            return

        for connection in self.active_connections[session_id]:
            try:
                await connection.send_text(json.dumps(message, ensure_ascii=False))
            except (RuntimeError, WebSocketDisconnect):
                self.disconnect(connection, session_id)
