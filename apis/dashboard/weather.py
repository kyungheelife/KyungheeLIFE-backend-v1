from fastapi import APIRouter
from app._weather import Weather, WheatherResponseModel


wt = APIRouter()

@wt.get(path='/openweathermap', response_model=WheatherResponseModel)
async def openweathermap():
    cl = Weather()
    return await cl.fetch()