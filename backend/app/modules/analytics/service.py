from typing import Any, Dict
from app.common.field_store import field_store


class AnalyticsModuleService:
    """数据分析模块服务封装。"""

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        fields = field_store.all()
        total_fields = len(fields)
        average_area = sum(field.get("area", 0) for field in fields) / total_fields if total_fields else 0
        average_moisture = sum(field.get("soil_moisture", 0) for field in fields) / total_fields if total_fields else 0
        average_temperature = sum(field.get("temperature", 0) for field in fields) / total_fields if total_fields else 0

        crop_types = {}
        for field in fields:
            crop_type = field.get("crop_type", "未知")
            crop_types[crop_type] = crop_types.get(crop_type, 0) + 1

        return {
            "total_fields": total_fields,
            "average_area": average_area,
            "average_moisture": average_moisture,
            "average_temperature": average_temperature,
            "crop_distribution": crop_types,
        }
