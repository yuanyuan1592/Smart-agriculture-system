from datetime import datetime
from typing import List
from pydantic import BaseModel


class WeatherForecastItem(BaseModel):
    day: str
    condition: str
    low: float
    high: float
    wind_direction: str
    wind_strength: str
    aqi: int
    uv_index: int
    air_quality: str


class WeatherItem(BaseModel):
    id: int
    location: str
    temperature: float
    humidity: float
    wind_direction: str
    wind_strength: str
    air_quality: str
    aqi: int
    uv_index: int
    condition: str
    forecast: List[WeatherForecastItem]
    disaster_predictions: List[str]
    generated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class WeatherResponse(BaseModel):
    generated_at: datetime
    weather: List[WeatherItem]

    model_config = {
        "from_attributes": True,
    }
