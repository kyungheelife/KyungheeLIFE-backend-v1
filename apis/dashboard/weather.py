from fastapi import APIRouter
from app._weather import Weather, WhetherResponseModel


wt = APIRouter()

@wt.get(path='/openweathermap', response_model=WhetherResponseModel)
async def openweathermap():
    cl = Weather()
    return await cl.fetch()