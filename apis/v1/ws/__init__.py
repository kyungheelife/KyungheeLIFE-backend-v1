from fastapi import APIRouter
from apis.v1.ws.dashboard import dash_root_router

dashboard = APIRouter()
dashboard.include_router(dash_root_router, prefix="/dashboard", tags=["dashboard"])
