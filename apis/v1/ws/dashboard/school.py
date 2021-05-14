from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.modules import School
from app.modules import ReturnErrorMSG
from app.manager import ConnectionManager

school_route = APIRouter()


@school_route.websocket_route("/lunch")
async def lunch(websocket: WebSocket):

    sc = School()
    async with ConnectionManager(websocket=websocket) as ex:
        try:
            while 1:
                try:
                    resp = await ex.ping()
                    if resp.get("message") != "ping":
                        break
                    nx = await sc.fetchLunch()
                    data = nx.strip()
                    res = {
                        "status": True,
                        "system": {
                            "code": 200,
                            "message": "OK"
                        },
                        "data": [*data]
                    }
                    await ex.broadcast(message=res)
                except Exception as e:
                    print("error:", e)
                    break
        except WebSocketDisconnect as e:
            msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
            await ex.broadcast(message=msg)


@school_route.websocket_route("/dinner")
async def dinner(websocket: WebSocket):
    sc = School()
    async with ConnectionManager(websocket=websocket) as ex:
        try:
            while 1:
                try:
                    resp = await ex.ping()
                    if resp.get("message") != "ping":
                        break
                    nx = await sc.fetchDinner()
                    data = nx.strip()
                    res = {
                        "status": True,
                        "system": {
                            "code": 200,
                            "message": "OK"
                        },
                        "data": [*data]
                    }
                    await ex.broadcast(message=res)
                except Exception as e:
                    print("error:", e)
                    break
        except WebSocketDisconnect as e:
            msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
            await ex.broadcast(message=msg)
