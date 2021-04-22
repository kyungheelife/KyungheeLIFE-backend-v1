from fastapi import APIRouter
from app.school import School

meals = APIRouter()


@meals.get("/lunch")
async def lunch():
    sc = School()
    nx = await sc.fetch_meal()
    return [*nx[0].split()]


@meals.get("/dinner")
async def dinner():
    sc = School()
    nx = await sc.fetch_meal()
    return [*nx[1].split()]
