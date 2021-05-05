from fastapi import APIRouter
from .meal import meals
from .weather import wt
from .covid import covid
dashboard = APIRouter(prefix="/dashboard")

dashboard.include_router(meals, prefix="/meals")
dashboard.include_router(wt, prefix="/weather")
dashboard.include_router(covid, prefix="/covid19")
