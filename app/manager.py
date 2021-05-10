from typing import List
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: dict):
        for connection in self.connections:
            await connection.send_json(data)


manager = ConnectionManager()

__all__ = (
    "manager"
)
