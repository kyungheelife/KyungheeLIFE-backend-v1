from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect
from app.modules import CovidStats
from app.modules import ReturnErrorMSG
from app.manager import ConnectionManager
from app.services import timestamp

covid_route = APIRouter()


@covid_route.websocket_route("/total")
async def covid_total(websocket: WebSocket):
    async with ConnectionManager(websocket=websocket) as ex:
        try:
            try:
                c = CovidStats()
                while 1:
                    try:
                        resp = await websocket.receive_json()
                        if resp.get("message") != "ping":
                            break

                        res = await c.ROKTotals()
                        res.update({"timestamp": timestamp()})
                        await ex.broadcast(message=res)
                    except Exception as e:
                        print(f"[ERROR]: [{e}]")
                        await ex.broadcast(
                            message=dict(
                                ReturnErrorMSG(
                                    status=False,
                                    code=500,
                                    message="[ERROR] Internal Server Error"
                                ).__dict__
                            )
                        )
                        break

            except WebSocketDisconnect as e:
                print(f"[ERROR]: [{e.code}]")
                await ex.broadcast(
                    message=dict(
                        ReturnErrorMSG(
                            status=False,
                            code=e.code,
                            message="Disconnected"
                        ).__dict__
                    )
                )
        except Exception as e:
            print(f"[ERROR]: [{e}]")
            await ex.broadcast(
                message=dict(
                    ReturnErrorMSG(
                        status=False,
                        code=500,
                        message="[ERROR] Internal Server Error"
                    ).__dict__
                )
            )
