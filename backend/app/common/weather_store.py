from datetime import datetime
from typing import Any, Dict, List
import re


class WeatherStore:
    """公共天气存储，提供模拟天气和灾害预警数据。"""

    def __init__(self) -> None:
        self._weather: List[Dict[str, Any]] = []
        self._initialize_mock_data()

    @staticmethod
    def _parse_wind_level(wind_strength: str) -> int:
        match = re.search(r"(\d+)", wind_strength or "")
        return int(match.group(1)) if match else 0

    def _build_disaster_predictions(self, weather: Dict[str, Any]) -> List[str]:
        predictions: List[str] = []
        temperature = weather.get("temperature", 0)
        humidity = weather.get("humidity", 0)
        aqi = weather.get("aqi", 0)
        uv_index = weather.get("uv_index", 0)
        wind_strength = self._parse_wind_level(weather.get("wind_strength", ""))
        condition = weather.get("condition", "")

        if temperature >= 38:
            predictions.append("极端高温预警")
        elif temperature >= 35:
            predictions.append("高温预警")

        if temperature <= 0:
            predictions.append("严寒预警")
        elif temperature <= 5:
            predictions.append("低温预警")

        if humidity <= 20:
            predictions.append("干旱预警")
        elif humidity >= 95 or "暴雨" in condition or "雷雨" in condition:
            predictions.append("洪涝预警")

        if wind_strength >= 7 or "强风" in condition:
            predictions.append("强风预警")

        if aqi >= 200:
            predictions.append("重度空气污染预警")
        elif aqi >= 150:
            predictions.append("空气质量差，注意防护")

        if uv_index >= 9:
            predictions.append("紫外线指数极高，减少户外作业")
        elif uv_index >= 8:
            predictions.append("紫外线强烈，注意防晒")

        return predictions

    @staticmethod
    def _build_light_advice(weather: Dict[str, Any]) -> str:
        temperature = weather.get("temperature", 0)
        humidity = weather.get("humidity", 0)
        uv_index = weather.get("uv_index", 0)
        if uv_index >= 9 or temperature >= 35:
            return "强烈光照，建议做好遮阳与补水"
        if uv_index >= 7 or humidity <= 35:
            return "光照较强，适合适度补光"
        return "当前光照条件较稳定"

    @staticmethod
    def _build_agri_advice(weather: Dict[str, Any]) -> Dict[str, str]:
        temperature = weather.get("temperature", 0)
        humidity = weather.get("humidity", 0)
        condition = weather.get("condition", "")
        return {
            "irrigation": "建议适度灌溉，避开高温时段" if temperature >= 30 else "当前湿度较适宜，保持现有灌溉节奏",
            "spraying": "建议暂停喷药，等待风力变小后再操作" if "风" in condition or weather.get("wind_strength", "") != "" else "适合进行病虫害防治作业",
            "harvest": "适合安排采收，注意避开强降雨" if temperature >= 24 and humidity <= 80 else "建议继续观察作物成熟度",
        }

    def _initialize_mock_data(self) -> None:
        mock_weather = [
            {
                "id": 1,
                "location": "北园区",
                "temperature": 33.2,
                "humidity": 28,
                "wind_direction": "东南",
                "wind_strength": "3级",
                "air_quality": "良",
                "aqi": 68,
                "uv_index": 8,
                "condition": "晴朗",
                "forecast": [
                    {
                        "day": "今天",
                        "condition": "晴到多云",
                        "low": 22,
                        "high": 34,
                        "wind_direction": "东南",
                        "wind_strength": "3-4级",
                        "aqi": 72,
                        "uv_index": 8,
                        "air_quality": "良",
                    },
                    {
                        "day": "明天",
                        "condition": "晴热",
                        "low": 24,
                        "high": 36,
                        "wind_direction": "南",
                        "wind_strength": "3-4级",
                        "aqi": 95,
                        "uv_index": 9,
                        "air_quality": "良",
                    },
                    {
                        "day": "后天",
                        "condition": "多云",
                        "low": 23,
                        "high": 31,
                        "wind_direction": "东南",
                        "wind_strength": "2-3级",
                        "aqi": 88,
                        "uv_index": 7,
                        "air_quality": "良",
                    },
                ],
            },
            {
                "id": 2,
                "location": "东园区",
                "temperature": 25.8,
                "humidity": 86,
                "wind_direction": "东",
                "wind_strength": "5级",
                "air_quality": "轻度污染",
                "aqi": 155,
                "uv_index": 6,
                "condition": "多云",
                "forecast": [
                    {
                        "day": "今天",
                        "condition": "多云间晴",
                        "low": 21,
                        "high": 27,
                        "wind_direction": "东",
                        "wind_strength": "4-5级",
                        "aqi": 160,
                        "uv_index": 6,
                        "air_quality": "轻度污染",
                    },
                    {
                        "day": "明天",
                        "condition": "雷阵雨",
                        "low": 22,
                        "high": 28,
                        "wind_direction": "东南",
                        "wind_strength": "5-6级",
                        "aqi": 145,
                        "uv_index": 5,
                        "air_quality": "良",
                    },
                    {
                        "day": "后天",
                        "condition": "暴雨",
                        "low": 20,
                        "high": 25,
                        "wind_direction": "东南",
                        "wind_strength": "6-7级",
                        "aqi": 130,
                        "uv_index": 4,
                        "air_quality": "良",
                    },
                ],
            },
            {
                "id": 3,
                "location": "南园区",
                "temperature": 11.4,
                "humidity": 18,
                "wind_direction": "北",
                "wind_strength": "6级",
                "air_quality": "优",
                "aqi": 42,
                "uv_index": 3,
                "condition": "晴朗",
                "forecast": [
                    {
                        "day": "今天",
                        "condition": "晴朗",
                        "low": 6,
                        "high": 13,
                        "wind_direction": "北",
                        "wind_strength": "5-6级",
                        "aqi": 48,
                        "uv_index": 4,
                        "air_quality": "优",
                    },
                    {
                        "day": "明天",
                        "condition": "晴到多云",
                        "low": 8,
                        "high": 15,
                        "wind_direction": "东北",
                        "wind_strength": "4-5级",
                        "aqi": 58,
                        "uv_index": 5,
                        "air_quality": "优",
                    },
                    {
                        "day": "后天",
                        "condition": "晴朗",
                        "low": 7,
                        "high": 16,
                        "wind_direction": "东北",
                        "wind_strength": "4级",
                        "aqi": 54,
                        "uv_index": 5,
                        "air_quality": "优",
                    },
                ],
            },
            {
                "id": 4,
                "location": "西园区",
                "temperature": 29.6,
                "humidity": 92,
                "wind_direction": "西南",
                "wind_strength": "7级",
                "air_quality": "良",
                "aqi": 82,
                "uv_index": 7,
                "condition": "雷阵雨",
                "forecast": [
                    {
                        "day": "今天",
                        "condition": "雷阵雨",
                        "low": 24,
                        "high": 30,
                        "wind_direction": "西南",
                        "wind_strength": "6-7级",
                        "aqi": 85,
                        "uv_index": 6,
                        "air_quality": "良",
                    },
                    {
                        "day": "明天",
                        "condition": "暴雨",
                        "low": 22,
                        "high": 28,
                        "wind_direction": "西",
                        "wind_strength": "7-8级",
                        "aqi": 90,
                        "uv_index": 5,
                        "air_quality": "良",
                    },
                    {
                        "day": "后天",
                        "condition": "多云",
                        "low": 23,
                        "high": 29,
                        "wind_direction": "西北",
                        "wind_strength": "4-5级",
                        "aqi": 88,
                        "uv_index": 6,
                        "air_quality": "良",
                    },
                ],
            },
        ]

        for weather in mock_weather:
            weather["generated_at"] = datetime.utcnow()
            weather["disaster_predictions"] = self._build_disaster_predictions(weather)
            weather["light_advice"] = self._build_light_advice(weather)
            weather["agri_advice"] = self._build_agri_advice(weather)
            self._weather.append(weather)

    def all(self) -> List[Dict[str, Any]]:
        return self._weather

    def get(self, weather_id: int) -> Dict[str, Any] | None:
        for item in self._weather:
            if item.get("id") == weather_id:
                return item
        return None


weather_store = WeatherStore()
