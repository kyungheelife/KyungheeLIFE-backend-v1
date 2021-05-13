from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.modules import School
from app.modules import ReturnErrorMSG
from app.manager import manager

school_route = APIRouter()


@school_route.websocket_route("/lunch")
async def lunch(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        sc = School()
        while 1:
            try:
                resp = await websocket.receive_json()
                if resp.get("message") != "ping":
                    break
                nx = await sc.fetch_meal()
                data = nx[0].split()
                res = {
                    "status": True,
                    "system": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": [*data]
                }
                await manager.broadcast(message=res)
            except Exception as e:
                print("error:", e)
                break
    except WebSocketDisconnect as e:
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)
        manager.disconnect(websocket)


@school_route.websocket_route("/dinner")
async def dinner(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        sc = School()
        while 1:
            try:
                resp = await websocket.receive_json()
                if resp.get("message") != "ping":
                    break
                nx = await sc.fetch_meal()
                data = nx[1].split()
                res = {
                    "status": True,
                    "system": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": [*data]
                }
                await manager.broadcast(message=res)
            except Exception as e:
                print("error:", e)
                break
    except WebSocketDisconnect as e:
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)
        manager.disconnect(websocket)
