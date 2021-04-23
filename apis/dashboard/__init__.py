from fastapi import APIRouter
from .meal import meals
from .weather import wt

dashboard = APIRouter(prefix="/dashboard")

dashboard.include_router(meals, prefix="/meals")
dashboard.include_router(wt, prefix="/weather")