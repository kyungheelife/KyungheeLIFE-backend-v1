import typing
from aiohttp import ClientSession
from pydantic import BaseModel
from .config import W_API_KEY

class ReturnErrorMSG:
    """

    example:
        {
            "status": bool,
            "system": {
                "code": int,
                "message": str
            },
            "data": None,
        }
    """
    def __init__(self, status: bool, code: int, message: str) -> None:
        self.status: bool = status
        self.http_status_code: int = code
        self.message: str = message

    def __dict__(self) -> dict:
        return {
            "status": self.status,
            "system": {
                "code": self.http_status_code,
                "message": self.message
            },
            "data": None,
        }


class Weather:
    """Weather
    ================

    OpenWeatherMap API Warraper.
    .. OpenWeatherMap: https://openweathermap.org/
    """
    def __init__(self) -> None:
        self.appId: str = W_API_KEY
        self.api_url: str = "https://api.openweathermap.org/data/2.5/weather"
        self.query: dict = {
            "q": "Seoul",
            "units": "metric",
            "lang": "kr",
            "appid": self.appId
        }
    
    async def fetch(self) -> dict:
        async with ClientSession() as session:
            async with session.get(url=self.api_url, params=self.query) as resp:
                if resp.status != 200:
                    return ReturnErrorMSG(
                        status=False, 
                        code=resp.status, 
                        message="[ERROR] OpenWeatherMap API Request Failed."
                        ).__dict__()

                data: dict = await resp.json()
                    
                main: dict = data.get("main")
                __weather: list = data.get("weather")            
                weather = __weather[0]

                return {
                    "status": True,
                    "system": {
                        "code": resp.status,
                        "message": "OK"
                    },
                    "data": {
                        "main": main,
                        "weather": weather
                    }
                }
 

class systemModel(BaseModel):
    code: int
    message: str

class mainModel(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int

class weatherModel(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class dataModel(BaseModel):
    main: mainModel
    weather: weatherModel

class WheatherResponseModel(BaseModel):
     status: bool
     system: systemModel
     data: typing.Optional[dataModel]


__all__ = [
    "WheatherResponseModel",
    "Weather"
]
