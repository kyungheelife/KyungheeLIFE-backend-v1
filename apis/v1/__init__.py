from fastapi import APIRouter
from apis.v1.ws import dashboard


ws_route = APIRouter()
ws_route.include_router(dashboard, prefix="/ws", tags=["websocket"])
