from typing import Any, Dict, List


def build_detection_report(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """公共检测报告生成器。"""
    total_fields = len(fields)
    if total_fields == 0:
        return {
            "total_fields": 0,
            "average_moisture": 0,
            "average_temperature": 0,
            "field_status": []
        }

    total_moisture = sum(field.get("soil_moisture", 0) for field in fields)
    total_temperature = sum(field.get("temperature", 0) for field in fields)
    field_status = [
        {
            "id": field.get("id"),
            "name": field.get("name"),
            "status": "normal" if field.get("soil_moisture", 0) >= 30 else "dry"
        }
        for field in fields
    ]

    return {
        "total_fields": total_fields,
        "average_moisture": total_moisture / total_fields,
        "average_temperature": total_temperature / total_fields,
        "field_status": field_status,
    }
