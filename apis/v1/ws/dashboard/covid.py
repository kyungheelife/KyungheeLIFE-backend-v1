from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.modules import CovidStats
from app.modules import ReturnErrorMSG
from app.manager import manager

covid_route = APIRouter()


@covid_route.websocket_route("/total")
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
                continue
    except WebSocketDisconnect as e:
        msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
        await manager.broadcast(message=msg)
        manager.disconnect(websocket)
