import asyncio
from starlette.websockets import WebSocket
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
    port=8074,
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
    c = CovidStats()
    while 1:
        await asyncio.sleep(0.1)
        await websocket.receive_text()
        res = await c.ROKTotals()
        await manager.broadcast(data=res)


@core.app.websocket("/v1/ws/dashboard/school/lunch")
async def lunch(websocket: WebSocket):
    await manager.connect(websocket)
    sc = School()
    while 1:
        await asyncio.sleep(0.1)
        try:
            await websocket.receive_text()
            nx = await sc.fetch_meal()
            res = {
                "status": True,
                "system": {
                    "code": 200,
                    "message": "OK"
                },
                "data": [*nx[0].split()]
            }
            await manager.broadcast(data=res)
        except Exception:
            res = ReturnErrorMSG(
                status=False,
                code=500,
                message="[ERROR] NEIS API Request Failed."
            ).__dict__()
            await manager.broadcast(data=res)


@core.app.websocket("/v1/ws/dashboard/school/dinner")
async def dinner(websocket: WebSocket):
    await manager.connect(websocket)
    sc = School()
    while 1:
        await asyncio.sleep(0.1)
        try:
            await websocket.receive_text()
            nx = await sc.fetch_meal()
            res = {
                "status": True,
                "system": {
                    "code": 200,
                    "message": "OK"
                },
                "data": [*nx[1].split()]
            }
            await manager.broadcast(data=res)
        except Exception:
            res = ReturnErrorMSG(
                status=False,
                code=500,
                message="[ERROR] NEIS API Request Failed."
            ).__dict__()
            await manager.broadcast(data=res)


@core.app.websocket('/v1/ws/dashboard/weather/openweathermap')
async def openweathermap_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    source = Weather()
    while 1:
        await asyncio.sleep(0.1)
        try:
            res = await source.fetch()
            await manager.broadcast(data=res)
        except Exception as e:
            print("error: ", e)
            break

if __name__ == '__main__':
    core.start()
