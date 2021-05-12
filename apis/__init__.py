from fastapi import APIRouter
from apis.v1 import ws_route

v1 = APIRouter()
v1.include_router(ws_route, prefix="/v1", tags=["v1"])
