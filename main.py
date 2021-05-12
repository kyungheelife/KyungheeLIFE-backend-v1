from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware

from app.modules import School
from app.modules import Weather
from app.modules import CovidStats
from app.modules import ReturnErrorMSG

from app.controllers import KHSBackend
from app.manager import manager

# 127.0.0.1:8074/v1/ws/dashboard/weather/openweathermap

core = KHSBackend(
    host="0.0.0.0",
    port=3090,
    title="KyungheeLIFE BACKEND 3.0",
    description="KyungheeLIFE",
    debug=False
)


core.app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@core.app.websocket("/v1/ws/dashboard/covid19/total")
async def covid_total(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        c = CovidStats()
        while 1:
            try:
                resp = await websocket.receive_json()
                if resp.get("message") != "ping":
                    break
                res = await c.ROKTotals()
                await manager.broadcast(message=res)
            except Exception as e:
                print("error:", e)
                break
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)


@core.app.websocket("/v1/ws/dashboard/school/lunch")
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
                res = {
                    "status": True,
                    "system": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": [*nx[0].split()]
                }
                await manager.broadcast(message=res)
            except Exception as e:
                print("error:", e)
                break
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)


@core.app.websocket("/v1/ws/dashboard/school/dinner")
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
                res = {
                    "status": True,
                    "system": {
                        "code": 200,
                        "message": "OK"
                    },
                    "data": [*nx[1].split()]
                }
                await manager.broadcast(message=res)
            except Exception as e:
                print("error:", e)
                break
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)


@core.app.websocket('/v1/ws/dashboard/weather/openweathermap')
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
        manager.disconnect(websocket)
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)


if __name__ == '__main__':
    core.start()
