from fastapi import APIRouter
from apis.v1.ws.dashboard.covid import covid_route
from apis.v1.ws.dashboard.school import school_route
from apis.v1.ws.dashboard.weather import weather_route

dash_root_router = APIRouter()
dash_root_router.include_router(covid_route, prefix="/covid19")
dash_root_router.include_router(school_route, prefix="/school")
dash_root_router.include_router(weather_route, prefix="/weather")
