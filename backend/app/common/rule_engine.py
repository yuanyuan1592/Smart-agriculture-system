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
            light_intensity = field.get("light_intensity", 0)
            soil_ph = field.get("soil_ph", 0)
            if 60 <= moisture <= 90 and 20 <= temperature <= 30:
                warnings.append(f"{field.get('name', '未知农田')}：高湿高温，病虫害风险增加。")
            if moisture < 30 and temperature >= 28:
                warnings.append(f"{field.get('name', '未知农田')}：干热环境，病虫害可能爆发。")
            if moisture > 85 and temperature < 12:
                warnings.append(f"{field.get('name', '未知农田')}：潮湿低温，注意霉菌和根腐病。")
            if light_intensity < 6000 or light_intensity > 32000:
                warnings.append(f"{field.get('name', '未知农田')}：光照异常，需调整补光或遮阳。")
            if soil_ph < 5.5 or soil_ph > 8.0:
                warnings.append(f"{field.get('name', '未知农田')}：土壤酸碱度异常，需及时校正。")
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
    def build_trend_series(fields: List[Dict[str, Any]], days: int = 7) -> Dict[str, Any]:
        daily_data: Dict[str, Dict[str, Any]] = {}
        for field in fields:
            for record in field.get("history", []):
                timestamp = record.get("timestamp")
                if isinstance(timestamp, datetime):
                    date_str = timestamp.date().isoformat()
                else:
                    date_str = str(timestamp).split("T")[0]
                if date_str not in daily_data:
                    daily_data[date_str] = {"moisture": [], "temperature": [], "light": [], "ph": []}
                daily_data[date_str]["moisture"].append(record.get("soil_moisture", 0))
                daily_data[date_str]["temperature"].append(record.get("temperature", 0))
                daily_data[date_str]["light"].append(record.get("light_intensity", 0))
                daily_data[date_str]["ph"].append(record.get("soil_ph", 0))

        dates = sorted(daily_data.keys())
        if days is not None:
            dates = dates[-days:]
        trend = {
            "dates": dates,
            "avg_moisture": [],
            "avg_temperature": [],
            "avg_light": [],
            "avg_ph": [],
        }
        for date in dates:
            values = daily_data[date]
            trend["avg_moisture"].append(round(sum(values["moisture"]) / len(values["moisture"]), 1) if values["moisture"] else 0)
            trend["avg_temperature"].append(round(sum(values["temperature"]) / len(values["temperature"]), 1) if values["temperature"] else 0)
            trend["avg_light"].append(round(sum(values["light"]) / len(values["light"]), 1) if values["light"] else 0)
            trend["avg_ph"].append(round(sum(values["ph"]) / len(values["ph"]), 2) if values["ph"] else 0)
        return trend

    @staticmethod
    def build_trend_series_per_field(fields: List[Dict[str, Any]], days: int = 7) -> Dict[str, Any]:
        """Return per-field trend series keyed by field id. Dates are the union
        of all dates found across fields, sliced to the requested days for a
        consistent x-axis across charts."""
        # First build global date list using existing logic
        global_daily = {}
        for field in fields:
            for record in field.get("history", []):
                timestamp = record.get("timestamp")
                if isinstance(timestamp, datetime):
                    date_str = timestamp.date().isoformat()
                else:
                    date_str = str(timestamp).split("T")[0]
                global_daily.setdefault(date_str, True)
        dates = sorted(global_daily.keys())
        if days is not None:
            dates = dates[-days:]

        per_field = {}
        for field in fields:
            fid = field.get("id") or field.get("name")
            # map date -> values for this field
            data_by_date = {d: {"moisture": [], "temperature": [], "light": [], "ph": []} for d in dates}
            for record in field.get("history", []):
                timestamp = record.get("timestamp")
                if isinstance(timestamp, datetime):
                    date_str = timestamp.date().isoformat()
                else:
                    date_str = str(timestamp).split("T")[0]
                if date_str in data_by_date:
                    data_by_date[date_str]["moisture"].append(record.get("soil_moisture", 0))
                    data_by_date[date_str]["temperature"].append(record.get("temperature", 0))
                    data_by_date[date_str]["light"].append(record.get("light_intensity", 0))
                    data_by_date[date_str]["ph"].append(record.get("soil_ph", 0))

            trend = {"dates": dates, "avg_moisture": [], "avg_temperature": [], "avg_light": [], "avg_ph": []}
            for d in dates:
                vals = data_by_date[d]
                trend["avg_moisture"].append(round(sum(vals["moisture"]) / len(vals["moisture"]), 1) if vals["moisture"] else 0)
                trend["avg_temperature"].append(round(sum(vals["temperature"]) / len(vals["temperature"]), 1) if vals["temperature"] else 0)
                trend["avg_light"].append(round(sum(vals["light"]) / len(vals["light"]), 1) if vals["light"] else 0)
                trend["avg_ph"].append(round(sum(vals["ph"]) / len(vals["ph"]), 2) if vals["ph"] else 0)
            per_field[str(fid)] = trend
        return per_field
