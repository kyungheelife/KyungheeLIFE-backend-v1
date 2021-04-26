import json
import typing
from aiohttp import ClientSession
from app import ReturnErrorMSG
from .config import COVID_API_KEY


class CovidStats:
    def __init__(self) -> None:
        self.API_KEY = COVID_API_KEY
        self.api_url = "ncov.zeroday0619.dev/api/v3/"
