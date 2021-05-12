from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.manager import manager
from app.modules import Weather
from app.modules import ReturnErrorMSG


weather_route = APIRouter()


@weather_route.websocket_route('/openweathermap/')
async def openweathermap_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        source = Weather()
        while 1:
            try:
                resp = await websocket.receive_json()
                if resp.get("message") != "ping":
                    break
                res = await source.fetch()
                await manager.broadcast(message=res)
            except Exception as e:
                print("error: ", e)
                break
    except WebSocketDisconnect as e:
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)
        manager.disconnect(websocket)
