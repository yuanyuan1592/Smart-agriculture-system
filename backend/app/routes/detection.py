from typing import Any, Dict, List

from fastapi import APIRouter

from app.routes.field import fields_db

router = APIRouter()


def build_detection_report(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """基于农田监测数据生成农业检测报告。"""
    alerts: List[Dict[str, Any]] = []
    warning_count = 0
    critical_count = 0

    for field in fields:
        field_name = field.get("name", "未知农田")
        soil_moisture = field.get("soil_moisture", 0)
        temperature = field.get("temperature", 0)

        if soil_moisture < 35:
            alerts.append(
                {
                    "field_name": field_name,
                    "type": "warning",
                    "title": "土壤湿度偏低",
                    "message": f"{field_name} 的土壤湿度为 {soil_moisture}%，建议及时补水。",
                }
            )
            warning_count += 1
        elif soil_moisture > 70:
            alerts.append(
                {
                    "field_name": field_name,
                    "type": "warning",
                    "title": "土壤湿度偏高",
                    "message": f"{field_name} 的土壤湿度为 {soil_moisture}%，请注意排水。",
                }
            )
            warning_count += 1

        if temperature > 35:
            alerts.append(
                {
                    "field_name": field_name,
                    "type": "critical",
                    "title": "高温风险",
                    "message": f"{field_name} 的温度达到 {temperature}℃，建议加强遮阴与通风。",
                }
            )
            critical_count += 1
        elif temperature < 15:
            alerts.append(
                {
                    "field_name": field_name,
                    "type": "warning",
                    "title": "低温风险",
                    "message": f"{field_name} 的温度仅 {temperature}℃，建议采取保温措施。",
                }
            )
            warning_count += 1

    return {
        "summary": {
            "total_fields": len(fields),
            "warning_count": warning_count,
            "critical_count": critical_count,
            "healthy_count": max(len(fields) - warning_count - critical_count, 0),
        },
        "alerts": alerts,
    }


@router.get("/", response_model=Dict[str, Any])
async def get_detection_report():
    """获取农业检测报告。"""
    return build_detection_report(fields_db)
