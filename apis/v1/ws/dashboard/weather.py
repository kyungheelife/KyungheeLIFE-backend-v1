from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.manager import ConnectionManager
from app.modules import Weather
from app.modules import ReturnErrorMSG
from app.services import timestamp

weather_route = APIRouter()


@weather_route.websocket_route('/openweathermap')
async def openweathermap_endpoint(websocket: WebSocket):
    async with ConnectionManager(websocket=websocket) as ex:
        try:
            source = Weather()
            try:
                while 1:
                    try:
                        resp = await websocket.receive_json()
                        if resp.get("message") != "ping":
                            break
                        res = await source.fetch()
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
                print(f"[ERROR]: [{e}]")
                await ex.broadcast(
                    message=dict(
                        ReturnErrorMSG(
                            status=False,
                            code=e.code,
                            message="Disconnected!"
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
