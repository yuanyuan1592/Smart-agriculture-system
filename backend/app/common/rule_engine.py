from datetime import datetime
from typing import Any, Dict, List


class RuleEngine:
    @staticmethod
    def evaluate_irrigation(fields: List[Dict[str, Any]]) -> str:
        if not fields:
            return "暂无农田数据，无法给出灌溉建议。"

        dry_fields = [field for field in fields if field.get("soil_moisture", 0) < 35]
        wet_fields = [field for field in fields if field.get("soil_moisture", 0) > 70]
        if len(dry_fields) > len(wet_fields) and len(dry_fields) >= max(1, len(fields) // 3):
            return "多块农田偏干，请优先安排灌溉，并关注根区土壤含水率。"
        if len(wet_fields) > len(dry_fields) and len(wet_fields) >= max(1, len(fields) // 3):
            return "部分农田偏湿，建议暂停灌溉并检查排水，避免渍涝和病虫害。"
        return "当前土壤含水均衡，建议继续按计划灌溉并密切监测。"

    @staticmethod
    def evaluate_pest_risk(fields: List[Dict[str, Any]]) -> str:
        if not fields:
            return "暂无数据，无法评估病虫害风险。"

        warnings = []
        for field in fields:
            moisture = field.get("soil_moisture", 0)
            temperature = field.get("temperature", 0)
            if 60 <= moisture <= 90 and 20 <= temperature <= 30:
                warnings.append(f"{field.get('name', '未知农田')}：高湿高温，病虫害风险增加。")
            if moisture < 30 and temperature >= 28:
                warnings.append(f"{field.get('name', '未知农田')}：干热环境，病虫害可能爆发。")
            if moisture > 85 and temperature < 12:
                warnings.append(f"{field.get('name', '未知农田')}：潮湿低温，注意霉菌和根腐病。")
        if not warnings:
            return "当前病虫害风险较低，继续保持监测。"
        return "；".join(warnings[:3])

    @staticmethod
    def build_field_comparison(fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        comparison = []
        for field in fields:
            moisture = field.get("soil_moisture", 0)
            temperature = field.get("temperature", 0)
            moisture_low = field.get("moisture_threshold_low", 30.0)
            moisture_high = field.get("moisture_threshold_high", 70.0)
            temp_low = field.get("temperature_threshold_low", 15.0)
            temp_high = field.get("temperature_threshold_high", 35.0)
            comparison.append({
                "name": field.get("name", "未知农田"),
                "crop_type": field.get("crop_type", "未知"),
                "moisture": moisture,
                "temperature": temperature,
                "moisture_range": f"{moisture_low}%~{moisture_high}%",
                "temperature_range": f"{temp_low}℃~{temp_high}℃",
                "risk_level": field.get("status", "normal"),
                "moisture_status": "偏低" if moisture < moisture_low else "偏高" if moisture > moisture_high else "正常",
                "temperature_status": "偏低" if temperature < temp_low else "偏高" if temperature > temp_high else "正常",
            })
        return comparison

    @staticmethod
    def build_trend_series(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        daily_data: Dict[str, Dict[str, Any]] = {}
        for field in fields:
            for record in field.get("history", []):
                timestamp = record.get("timestamp")
                if isinstance(timestamp, datetime):
                    date_str = timestamp.date().isoformat()
                else:
                    date_str = str(timestamp).split("T")[0]
                if date_str not in daily_data:
                    daily_data[date_str] = {"moisture": [], "temperature": []}
                daily_data[date_str]["moisture"].append(record.get("soil_moisture", 0))
                daily_data[date_str]["temperature"].append(record.get("temperature", 0))

        dates = sorted(daily_data.keys())
        trend = {
            "dates": dates,
            "avg_moisture": [],
            "avg_temperature": [],
        }
        for date in dates:
            values = daily_data[date]
            trend["avg_moisture"].append(round(sum(values["moisture"]) / len(values["moisture"]), 1) if values["moisture"] else 0)
            trend["avg_temperature"].append(round(sum(values["temperature"]) / len(values["temperature"]), 1) if values["temperature"] else 0)
        return trend
