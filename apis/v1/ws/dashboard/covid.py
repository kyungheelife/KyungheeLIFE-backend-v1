from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.modules import CovidStats
from app.modules import ReturnErrorMSG
from app.manager import ConnectionManager

covid_route = APIRouter()


@covid_route.websocket_route("/total")
async def covid_total(websocket: WebSocket):
    try:
        c = CovidStats()
        async with ConnectionManager(websocket=websocket) as ex:
            try:
                while 1:
                    try:
                        resp = await websocket.receive_json()
                        if resp.get("message") != "ping":
                            break
                        res = await c.ROKTotals()
                        await ex.broadcast(message=res)
                    except Exception as e:
                        print("error:", e)
                        break

            except WebSocketDisconnect as e:
                msg = ReturnErrorMSG(status=False, code=e.code, message=f"Disconnected!").__dict__()
                await ex.broadcast(message=msg)
    except Exception as a:
        print("error:", a)
