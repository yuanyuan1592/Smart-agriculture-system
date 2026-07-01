from datetime import datetime, timezone
from typing import Any, Dict
from app.common.weather_store import weather_store


class WeatherModuleService:
    """天气模块服务封装。"""

    @staticmethod
    def get_weather() -> Dict[str, Any]:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "weather": weather_store.all(),
        }
