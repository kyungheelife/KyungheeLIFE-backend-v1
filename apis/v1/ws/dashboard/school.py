from fastapi import APIRouter

from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.modules import School
from app.modules import ReturnErrorMSG
from app.services import timestamp
from app.manager import ConnectionManager


school_route = APIRouter()


@school_route.websocket_route("/lunch")
async def lunch(websocket: WebSocket):
    async with ConnectionManager(websocket=websocket) as ex:
        try:
            sc = School()
            try:
                while 1:
                    try:
                        resp = await ex.ping()
                        if resp.get("message") != "ping":
                            break
                        nx = await sc.fetchLunch()
                        data = nx.split()
                        res = {
                            "status": True,
                            "system": {
                                "code": 200,
                                "message": "OK"
                            },
                            "data": [*data]
                        }
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
                            message=f"Disconnected!"
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


@school_route.websocket_route("/dinner")
async def dinner(websocket: WebSocket):
    async with ConnectionManager(websocket=websocket) as ex:
        try:
            sc = School()
            try:
                while 1:
                    try:
                        resp = await ex.ping()
                        if resp.get("message") != "ping":
                            break
                        nx = await sc.fetchDinner()
                        data = nx.split()
                        res = {
                            "status": True,
                            "system": {
                                "code": 200,
                                "message": "OK"
                            },
                            "data": [*data]
                        }
                        res.update({"timestamp": timestamp()})
                        await ex.broadcast(message=res)
                    except Exception as e:
                        print(f"[ERROR]: [{e}]")
                        await ex.broadcast(
                            message=dict(
                                ReturnErrorMSG(
                                    status=False,
                                    code=500,
                                    message="[ERROR] Internal Server Error").__dict__
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
                            message=f"Disconnected!"
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
                        message="[ERROR] Internal Server Error").__dict__
                )
            )
