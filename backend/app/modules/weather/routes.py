from fastapi import APIRouter
from typing import Any, Dict
from app.modules.weather.service import WeatherModuleService

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_weather() -> Dict[str, Any]:
    return WeatherModuleService.get_weather()
