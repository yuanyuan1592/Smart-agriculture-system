from datetime import datetime
from typing import Any, Dict, List


class FieldStore:
    """公共字段存储服务，供各模块调用。"""

    def __init__(self) -> None:
        self._fields: List[Dict[str, Any]] = []

    def all(self) -> List[Dict[str, Any]]:
        return self._fields

    def get(self, field_id: int) -> Dict[str, Any] | None:
        for field in self._fields:
            if field.get("id") == field_id:
                return field
        return None

    def create(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        current_time = datetime.utcnow()
        new_field = {
            "id": len(self._fields) + 1,
            "created_at": current_time,
            "updated_at": current_time,
            **field_data,
        }
        self._fields.append(new_field)
        return new_field

    def update(self, field_id: int, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        for index, field in enumerate(self._fields):
            if field.get("id") == field_id:
                self._fields[index].update(field_data)
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
