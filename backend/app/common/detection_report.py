from typing import Any, Dict, List
from app.common.weather_store import weather_store
from app.common.rule_engine import RuleEngine


def build_detection_report(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """公共检测报告生成器。"""
    summary = {
        "total_fields": 0,
        "warning_count": 0,
        "critical_count": 0,
        "healthy_count": 0,
        "weather_alert_count": 0,
        "pest_risk_summary": "",
    }
    alerts: List[Dict[str, Any]] = []

    def get_status(field_data: Dict[str, Any]) -> str:
        moisture = field_data.get("soil_moisture", 0)
        temperature = field_data.get("temperature", 0)
        if moisture <= 22 or temperature < 5 or temperature >= 38:
            return "alert"
        if moisture < 30 or temperature < 15 or temperature > 35 or moisture > 70:
            return "warning"
        return "normal"

    def _recommend_action(title: str, alert_type: str) -> str:
        if "干旱" in title:
            return "建议及时灌溉，补充水分并检查土壤含水状况。"
        if "湿度过高" in title or "洪涝" in title:
            return "建议暂停灌溉，检查排水并预防病虫害。"
        if "低温" in title or "严寒" in title:
            return "建议加强保温、防霜和覆盖保护。"
        if "高温" in title or "极端高温" in title:
            return "建议加强遮阳、补水并监控叶面蒸腾。"
        if "光照" in title:
            return "建议调整补光或遮阳措施，维持作物生长所需光照强度。"
        if "酸碱度" in title or "酸碱" in title:
            return "建议根据作物需求调节土壤酸碱度，必要时施用石灰或硫磺。"
        if "强风" in title:
            return "建议加固设施，移除松散物，防止风害。"
        if "空气污染" in title or "紫外线" in title:
            return "建议减少露天作业，做好防护。"
        return "建议关注当前预警，及时调整管理措施。"

    def append_alert(field_name: str, title: str, message: str, alert_type: str, source: str = "传感器", detail: str = "", field_id: int | None = None):
        alerts.append({
            "field_name": field_name,
            "title": title,
            "message": message,
            "type": alert_type,
            "source": source,
            "detail": detail,
            "recommendation": _recommend_action(title, alert_type),
            "field_id": field_id,
        })

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
        light_intensity = field.get("light_intensity", 0)
        soil_ph = field.get("soil_ph", 0)

        thresholds = {
            "moisture_low": field.get("moisture_threshold_low", 30.0),
            "moisture_high": field.get("moisture_threshold_high", 70.0),
            "temperature_low": field.get("temperature_threshold_low", 15.0),
            "temperature_high": field.get("temperature_threshold_high", 35.0),
            "light_low": field.get("light_threshold_low", 8000.0),
            "light_high": field.get("light_threshold_high", 30000.0),
            "ph_low": field.get("ph_threshold_low", 6.0),
            "ph_high": field.get("ph_threshold_high", 7.5),
        }

        if moisture <= 22:
            append_alert(
                field.get("name", ""),
                "土壤湿度偏低",
                "当前土壤湿度极低，可能出现旱情，请尽快灌溉。",
                "critical",
                "传感器",
                f"湿度 {moisture}%，阈值区间 {thresholds['moisture_low']}%~{thresholds['moisture_high']}%",
                field.get("id")
            )
        elif moisture < 30:
            append_alert(
                field.get("name", ""),
                "土壤湿度偏低",
                "当前土壤湿度偏低，建议及时灌溉。",
                "warning",
                "传感器",
                f"湿度 {moisture}%，阈值下限 {thresholds['moisture_low']}%",
                field.get("id")
            )

        if moisture > 90:
            append_alert(
                field.get("name", ""),
                "暴雨洪涝预警",
                "土壤湿度极高，存在洪涝和病虫害风险。",
                "critical",
                "传感器",
                f"湿度 {moisture}%，阈值上限 {thresholds['moisture_high']}%",
                field.get("id")
            )
        elif moisture > 70:
            append_alert(
                field.get("name", ""),
                "湿度过高",
                "当前土壤湿度较高，需警惕渍涝和病害。",
                "warning",
                "传感器",
                f"湿度 {moisture}%，阈值上限 {thresholds['moisture_high']}%",
                field.get("id")
            )

        if temperature < 5:
            append_alert(
                field.get("name", ""),
                "严寒预警",
                "当前温度极低，可能影响作物生长，建议采取保温措施。",
                "critical",
                "传感器",
                f"温度 {temperature}℃，阈值下限 {thresholds['temperature_low']}℃",
                field.get("id")
            )
        elif temperature < 15:
            append_alert(
                field.get("name", ""),
                "低温预警",
                "当前温度低于安全范围，可能影响作物发育。",
                "warning",
                "传感器",
                f"温度 {temperature}℃，阈值下限 {thresholds['temperature_low']}℃",
                field.get("id")
            )

        if temperature > 38:
            append_alert(
                field.get("name", ""),
                "极端高温预警",
                "当前温度非常高，可能对作物造成严重伤害。",
                "critical",
                "传感器",
                f"温度 {temperature}℃，阈值上限 {thresholds['temperature_high']}℃",
                field.get("id")
            )
        elif temperature > 35:
            append_alert(
                field.get("name", ""),
                "高温预警",
                "当前温度偏高，建议加强遮阳和补水。",
                "warning",
                "传感器",
                f"温度 {temperature}℃，阈值上限 {thresholds['temperature_high']}℃",
                field.get("id")
            )

        if light_intensity < thresholds["light_low"] * 0.7:
            append_alert(
                field.get("name", ""),
                "光照不足预警",
                "当前光照强度明显偏低，可能影响光合作用和生长速度。",
                "warning",
                "传感器",
                f"光照强度 {light_intensity}lux，建议维持在 {thresholds['light_low']}lux 以上",
                field.get("id")
            )
        elif light_intensity > thresholds["light_high"] * 1.15:
            append_alert(
                field.get("name", ""),
                "光照过强预警",
                "当前光照强度过高，可能导致灼伤或水分蒸发加快。",
                "warning",
                "传感器",
                f"光照强度 {light_intensity}lux，建议控制在 {thresholds['light_high']}lux 以下",
                field.get("id")
            )

        if soil_ph < thresholds["ph_low"] - 0.5:
            append_alert(
                field.get("name", ""),
                "土壤酸碱度偏低预警",
                "当前土壤偏酸，可能影响养分吸收和根系健康。",
                "warning",
                "传感器",
                f"土壤 pH {soil_ph}，适宜区间 {thresholds['ph_low']}~{thresholds['ph_high']}",
                field.get("id")
            )
        elif soil_ph > thresholds["ph_high"] + 0.3:
            append_alert(
                field.get("name", ""),
                "土壤酸碱度偏高预警",
                "当前土壤偏碱，可能抑制某些养分吸收。",
                "warning",
                "传感器",
                f"土壤 pH {soil_ph}，适宜区间 {thresholds['ph_low']}~{thresholds['ph_high']}",
                field.get("id")
            )

    for weather in weather_store.all():
        for prediction in weather.get("disaster_predictions", []):
            if "极端" in prediction or "严寒" in prediction or "洪涝" in prediction or "强风" in prediction:
                alert_type = "critical"
            else:
                alert_type = "warning"
            append_alert(weather.get("location", "气象预警"), prediction, "该预警来自天气预报，已自动触发并推送给用户。", alert_type, "气象预警")
            summary["weather_alert_count"] += 1

    summary["pest_risk_summary"] = RuleEngine.evaluate_pest_risk(fields)
    return {
        "summary": summary,
        "alerts": alerts,
    }
