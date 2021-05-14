from typing import List
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self, websocket: WebSocket) -> None:
        self._websocket = websocket
        self.active_connections: List[WebSocket] = []

    async def __aenter__(self):
        await self._connect(self._websocket)
        return self

    async def __aexit__(self, type, value, traceback):
        # print(f"{type}:{value}:{traceback}")
        await self._disconnect()

    async def _connect(self, websocket: WebSocket):
        await websocket.accept()
        return self.active_connections.append(websocket)

    async def _disconnect(self):
        return [self.active_connections.remove(connection) for connection in self.active_connections]

    async def broadcast(self, message: dict):
        return [await connection.send_json(message) for connection in self.active_connections]

    async def ping(self):
        resp = await self._websocket.receive_json()
        return resp

    @staticmethod
    async def send_personal_message(websocket: WebSocket, message: dict,):
        await websocket.send_json(message)


__all__ = (
    "ConnectionManager"
)
