from fastapi import APIRouter
from app.data_go_lr import CovidStats

covid = APIRouter()


@covid.get("/total")
async def covid_total():
    c = CovidStats()
    res = await c.ROKTotals()
    return res
