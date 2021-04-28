import typing
from pydantic import BaseModel
from neispy import Client
import datetime
import re

from .config import API_KEY


class School:
    def __init__(self):
        self.neis = Client(KEY=API_KEY)

    @staticmethod
    async def find(meal, nt):
        """급식 찾기

        :param meal: original data
        :param nt: 조식 중식 석식
        :return:
        """
        for bob in meal:
            if bob.get(nt):
                return bob.get(nt)
        return "해당하는\n데이터가\n없습니다."

    async def GetCode(self):
        KST = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(tz=KST)
        YMD = now.strftime("%Y%m%d")

        sc_info = await self.neis.schoolInfo(SCHUL_NM="경희고등학교")
        AE: str = sc_info[0]["ATPT_OFCDC_SC_CODE"]
        SE: str = sc_info[0]["SD_SCHUL_CODE"]
        return [AE, SE, YMD]

    async def fetch_meal(self):
        AE, SE, YMD = await self.GetCode()
        _meal = await self.neis.mealServiceDietInfo(AE, SE, MLSV_YMD=YMD)
        da = []
        _da = da.append
        p = re.compile("[^0-9]")
        for meal in _meal:
            _da(
                {
                    meal.MMEAL_SC_NM: "".join(
                        p.findall(
                            re.sub(
                                r"[-=.#/?:$}]",
                                "",
                                meal.DDISH_NM.replace(
                                    "<br/>",
                                    "\n"
                                )
                            )
                        )
                    )
                }
            )
        lu = await self.find(da, "중식")
        lk = await self.find(da, "석식")

        return [lu, lk]


class systemModel(BaseModel):
    code: int
    message: str


class MealResponseModel(BaseModel):
    status: bool
    system: systemModel
    data: typing.Optional[typing.List[str]]