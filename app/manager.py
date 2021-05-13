from typing import List
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        [await connection.send_json(message) for connection in self.active_connections]

    @staticmethod
    async def send_personal_message(websocket: WebSocket, message: dict,):
        await websocket.send_json(message)


manager = ConnectionManager()

__all__ = (
    "manager"
)
