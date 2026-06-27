from datetime import datetime, timedelta
from typing import Any, Dict, List


class FieldStore:
    """公共字段存储服务，供各模块调用。"""

    DEFAULT_MOISTURE_LOW = 30.0
    DEFAULT_MOISTURE_HIGH = 70.0
    DEFAULT_TEMPERATURE_LOW = 15.0
    DEFAULT_TEMPERATURE_HIGH = 35.0

    def __init__(self) -> None:
        self._fields: List[Dict[str, Any]] = []
        self._initialize_mock_data()

    def _get_status(self, field_data: Dict[str, Any]) -> str:
        moisture = field_data.get("soil_moisture", 0)
        temp = field_data.get("temperature", 0)
        moisture_low = field_data.get("moisture_threshold_low", self.DEFAULT_MOISTURE_LOW)
        moisture_high = field_data.get("moisture_threshold_high", self.DEFAULT_MOISTURE_HIGH)
        temp_low = field_data.get("temperature_threshold_low", self.DEFAULT_TEMPERATURE_LOW)
        temp_high = field_data.get("temperature_threshold_high", self.DEFAULT_TEMPERATURE_HIGH)

        if moisture < moisture_low * 0.7 or temp < temp_low - 10 or temp > temp_high + 3:
            return "alert"
        if moisture < moisture_low or moisture > moisture_high or temp < temp_low or temp > temp_high:
            return "warning"
        return "normal"

    def _generate_history_entries(self, field_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        now = datetime.utcnow()
        base_moisture = field_data.get("soil_moisture", 0)
        base_temperature = field_data.get("temperature", 0)
        history = []
        for day_offset in range(9, -1, -1):
            moisture_variation = base_moisture - (9 - day_offset) * 1.8
            temperature_variation = base_temperature - (9 - day_offset) * 0.8
            history.append({
                "timestamp": now - timedelta(days=day_offset),
                "soil_moisture": max(0.0, round(moisture_variation, 1)),
                "temperature": round(temperature_variation, 1),
            })
        return history

    def _default_thresholds(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "moisture_threshold_low": data.get("moisture_threshold_low", self.DEFAULT_MOISTURE_LOW),
            "moisture_threshold_high": data.get("moisture_threshold_high", self.DEFAULT_MOISTURE_HIGH),
            "temperature_threshold_low": data.get("temperature_threshold_low", self.DEFAULT_TEMPERATURE_LOW),
            "temperature_threshold_high": data.get("temperature_threshold_high", self.DEFAULT_TEMPERATURE_HIGH),
        }

    def _normalize_field(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        thresholds = self._default_thresholds(field_data)
        return {
            **field_data,
            **thresholds,
            "status": self._get_status(field_data),
            "last_measurement_at": datetime.utcnow(),
            "history": self._generate_history_entries(field_data),
        }

    def _initialize_mock_data(self) -> None:
        mock_fields = [
            {
                "name": "北区番茄田",
                "location": "北园区",
                "area": 12.5,
                "crop_type": "番茄",
                "soil_moisture": 28.0,
                "temperature": 22.0,
            },
            {
                "name": "东区玉米田",
                "location": "东园区",
                "area": 18.0,
                "crop_type": "玉米",
                "soil_moisture": 55.0,
                "temperature": 30.0,
            },
            {
                "name": "南区草莓园",
                "location": "南园区",
                "area": 8.7,
                "crop_type": "草莓",
                "soil_moisture": 72.0,
                "temperature": 26.0,
            },
            {
                "name": "西区白菜田",
                "location": "西园区",
                "area": 14.2,
                "crop_type": "白菜",
                "soil_moisture": 18.0,
                "temperature": 12.0,
            },
            {
                "name": "中区辣椒田",
                "location": "中园区",
                "area": 10.6,
                "crop_type": "辣椒",
                "soil_moisture": 62.0,
                "temperature": 31.5,
            },
            {
                "name": "温室草莓园",
                "location": "温室区",
                "area": 6.8,
                "crop_type": "草莓",
                "soil_moisture": 48.0,
                "temperature": 24.0,
            },
        ]
        for field in mock_fields:
            self.create(field)

    def all(self) -> List[Dict[str, Any]]:
        return self._fields

    def get(self, field_id: int) -> Dict[str, Any] | None:
        for field in self._fields:
            if field.get("id") == field_id:
                return field
        return None

    def create(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        current_time = datetime.utcnow()
        normalized = self._normalize_field(field_data)
        new_field = {
            "id": len(self._fields) + 1,
            "created_at": current_time,
            "updated_at": current_time,
            **normalized,
        }
        self._fields.append(new_field)
        return new_field

    def update(self, field_id: int, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        for index, field in enumerate(self._fields):
            if field.get("id") == field_id:
                self._fields[index].update(field_data)
                self._fields[index].update(self._default_thresholds(self._fields[index]))
                self._fields[index]["status"] = self._get_status(self._fields[index])
                self._fields[index]["updated_at"] = datetime.utcnow()
                self._fields[index]["last_measurement_at"] = datetime.utcnow()
                current_history = self._fields[index].get("history", [])
                current_history.insert(0, {
                    "timestamp": self._fields[index]["last_measurement_at"],
                    "soil_moisture": round(self._fields[index].get("soil_moisture", 0), 1),
                    "temperature": round(self._fields[index].get("temperature", 0), 1),
                })
                self._fields[index]["history"] = current_history[:30]
                return self._fields[index]
        return None

    def delete(self, field_id: int) -> bool:
        for index, field in enumerate(self._fields):
            if field.get("id") == field_id:
                self._fields.pop(index)
                return True
        return False


field_store = FieldStore()
