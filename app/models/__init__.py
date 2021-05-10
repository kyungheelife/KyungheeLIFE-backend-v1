from typing import Optional, List
from pydantic import BaseModel


# Global model
class systemModel(BaseModel):
    """This class is Global Model"""
    code: int
    message: str


# ROOT Model
class MealResponseModel(BaseModel):
    """This class is ROOT Model"""
    status: bool
    system: systemModel
    data: Optional[List[str]]


class mainWeatherModel(BaseModel):
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
    main: mainWeatherModel
    weather: weatherModel


# ROOT Model
class WhetherResponseModel(BaseModel):
    """This class is ROOT Model"""
    status: bool
    system: systemModel
    data: Optional[dataModel]


__all__ = (
    "systemModel",
    "MealResponseModel",
    "WhetherResponseModel",
    "dataModel",
    "weatherModel",
    "mainWeatherModel"
)
