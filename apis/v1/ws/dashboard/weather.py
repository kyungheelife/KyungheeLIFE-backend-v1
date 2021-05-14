from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.manager import ConnectionManager
from app.modules import Weather
from app.modules import ReturnErrorMSG


weather_route = APIRouter()


@weather_route.websocket_route('/openweathermap')
async def openweathermap_endpoint(websocket: WebSocket):
    try:
        source = Weather()
        async with ConnectionManager(websocket=websocket) as ex:
            try:
                while 1:
                    try:
                        resp = await websocket.receive_json()
                        if resp.get("message") != "ping":
                            break
                        res = await source.fetch()
                        await ex.broadcast(message=res)
                    except Exception as e:
                        print("error: ", e)
                        break
            except WebSocketDisconnect as e:
                msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
                await ex.broadcast(message=msg)
    except Exception as a:
        print("error:", a)
