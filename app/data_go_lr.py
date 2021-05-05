from aiohttp import ClientSession
from app import ReturnErrorMSG
from .config import COVID_API_KEY


class CovidStats:
    def __init__(self) -> None:
        self.API_KEY = COVID_API_KEY
        self.api_url = "http://127.0.0.1:8899/api/v3/"

    async def ROKTotals(self):
        url = self.api_url + "kr/total"
        async with ClientSession() as session:
            try:
                async with session.get(url=url) as resp:
                    if resp.status != 200:
                        if resp.status != 500:
                            return resp.json()
                        return ReturnErrorMSG(status=False, code=resp.status, message="ERROR").__dict__()
                    response = await resp.json()
            except Exception as e:
                return ReturnErrorMSG(status=False, code=500, message="Internal Server Error").__dict__()

            return response

