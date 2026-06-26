from datetime import datetime
from typing import Any, Dict, List


class FieldStore:
    """公共字段存储服务，供各模块调用。"""

    def __init__(self) -> None:
        self._fields: List[Dict[str, Any]] = []
        self._initialize_mock_data()

    def _get_status(self, field_data: Dict[str, Any]) -> str:
        moisture = field_data.get("soil_moisture", 0)
        temp = field_data.get("temperature", 0)
        if moisture < 30 or temp < 15 or temp > 35:
            return "warning"
        if moisture > 70:
            return "alert"
        return "normal"

    def _normalize_field(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **field_data,
            "status": self._get_status(field_data),
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
                self._fields[index]["status"] = self._get_status(self._fields[index])
                self._fields[index]["updated_at"] = datetime.utcnow()
                return self._fields[index]
        return None

    def delete(self, field_id: int) -> bool:
        for index, field in enumerate(self._fields):
            if field.get("id") == field_id:
                self._fields.pop(index)
                return True
        return False


field_store = FieldStore()
