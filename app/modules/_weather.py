from aiohttp import ClientSession
from cachetools import TTLCache
from asyncache import cached

from app.config import W_API_KEY
from app.modules._error import ReturnErrorMSG


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

    @cached(TTLCache(maxsize=120, ttl=3600))
    async def fetch(self):
        async with ClientSession() as session:
            async with session.get(url=self.api_url, params=self.query) as resp:
                if resp.status != 200:
                    return dict(ReturnErrorMSG(
                        status=False,
                        code=resp.status,
                        message="[ERROR] OpenWeatherMap API Request Failed."
                    ).__dict__)

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


__all__ = (
    "Weather"
)
