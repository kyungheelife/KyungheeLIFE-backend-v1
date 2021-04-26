from fastapi import APIRouter
from app.school import School
from app import ReturnErrorMSG
from app.school import MealResponseModel

meals = APIRouter()


@meals.get("/lunch", response_model=MealResponseModel)
async def lunch():
    try:
        sc = School()
        nx = await sc.fetch_meal()
        return {
            "status": True,
            "system": {
                "code": 200,
                "message": "OK"
            },
            "data": [*nx[0].split()]
        }
    except Exception:
        return ReturnErrorMSG(
            status=False,
            code=500,
            message="[ERROR] NEIS API Request Failed."
        )


@meals.get("/dinner", response_model=MealResponseModel)
async def dinner():
    try:
        sc = School()
        nx = await sc.fetch_meal()
        return {
            "status": True,
            "system": {
                "code": 200,
                "message": "OK"
            },
            "data": [*nx[1].split()]
        }
    except Exception:
        return ReturnErrorMSG(
            status=False,
            code=500,
            message="[ERROR] NEIS API Request Failed."
        )
