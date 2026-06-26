from typing import Any, Dict, List


def build_detection_report(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """公共检测报告生成器。"""
    summary = {
        "total_fields": 0,
        "warning_count": 0,
        "critical_count": 0,
        "healthy_count": 0,
    }
    alerts: List[Dict[str, Any]] = []

    def get_status(field_data: Dict[str, Any]) -> str:
        moisture = field_data.get("soil_moisture", 0)
        temperature = field_data.get("temperature", 0)
        if moisture < 30 or temperature < 15 or temperature > 35:
            return "warning"
        if moisture > 70:
            return "alert"
        return "normal"

    for field in fields:
        summary["total_fields"] += 1
        status = get_status(field)

        if status == "normal":
            summary["healthy_count"] += 1
        else:
            summary["warning_count"] += 1

        if status == "alert":
            summary["critical_count"] += 1

        moisture = field.get("soil_moisture", 0)
        temperature = field.get("temperature", 0)

        if moisture < 30:
            alerts.append({
                "field_name": field.get("name", ""),
                "title": "土壤湿度偏低",
                "message": "当前土壤湿度低于安全阈值，建议及时灌溉。",
                "type": "warning" if status != "alert" else "critical",
            })

        if moisture > 70:
            alerts.append({
                "field_name": field.get("name", ""),
                "title": "土壤湿度偏高",
                "message": "当前土壤湿度过高，可能导致病虫害。",
                "type": "critical",
            })

        if temperature < 15:
            alerts.append({
                "field_name": field.get("name", ""),
                "title": "温度偏低",
                "message": "当前温度低于安全范围，可能影响作物生长。",
                "type": "warning",
            })

        if temperature > 35:
            alerts.append({
                "field_name": field.get("name", ""),
                "title": "温度偏高",
                "message": "当前温度超过安全阈值，建议降温或遮阴。",
                "type": "critical",
            })

    return {
        "summary": summary,
        "alerts": alerts,
    }
