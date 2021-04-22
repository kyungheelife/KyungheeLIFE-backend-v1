from fastapi import APIRouter
from .dashboard import dashboard

v1 = APIRouter(prefix="/v1")
v1.include_router(dashboard, tags=["dashboard"])
