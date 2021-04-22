from fastapi import APIRouter
from .meal import meals

dashboard = APIRouter(prefix="/dashboard")

dashboard.include_router(meals, prefix="/meals")