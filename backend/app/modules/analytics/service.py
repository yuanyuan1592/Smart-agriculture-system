from typing import Any, Dict
from app.common.field_store import field_store
from app.common.rule_engine import RuleEngine


class AnalyticsModuleService:
    """数据分析模块服务封装。"""

    @staticmethod
    def _growth_prediction(fields: list[dict[str, Any]]) -> str:
        if not fields:
            return "暂无数据可预测"

        avg_moisture = sum(field.get("soil_moisture", 0) for field in fields) / len(fields)
        avg_temperature = sum(field.get("temperature", 0) for field in fields) / len(fields)

        if 40 <= avg_moisture <= 70 and 20 <= avg_temperature <= 30:
            return "生长良好，当前环境适宜。"
        if avg_moisture < 35 or avg_temperature < 15 or avg_temperature > 35:
            return "生长环境不稳定，需及时调整水肥和温度管理。"
        return "生长趋势一般，建议保持当前管理并密切监测。"

    @staticmethod
    def _estimated_yield(fields: list[dict[str, Any]]) -> float:
        crop_factors = {
            "番茄": 0.8,
            "玉米": 1.2,
            "草莓": 0.9,
            "白菜": 1.0,
            "未知": 0.7,
        }
        total_estimate = 0.0
        for field in fields:
            factor = crop_factors.get(field.get("crop_type", "未知"), 0.8)
            health_multiplier = 1.0
            status = field.get("status", "normal")
            if status == "warning":
                health_multiplier = 0.88
            elif status == "alert":
                health_multiplier = 0.75
            total_estimate += field.get("area", 0) * factor * health_multiplier
        return round(total_estimate, 1)

    @staticmethod
    def _fertilizer_advice(fields: list[dict[str, Any]]) -> str:
        if not fields:
            return "暂无数据，无法给出肥水建议。"
        avg_moisture = sum(field.get("soil_moisture", 0) for field in fields) / len(fields)
        if avg_moisture < 35:
            return "土壤偏干，建议增加灌溉并适量补充氮磷钾肥。"
        if avg_moisture > 70:
            return "土壤偏湿，建议减少浇水，控制肥料用量，避免渍涝。"
        return "当前土壤湿度适中，可按常规肥水管理。"

    @staticmethod
    def _irrigation_advice(fields: list[dict[str, Any]]) -> str:
        if not fields:
            return "暂无数据，无法给出灌溉建议。"
        low_count = sum(1 for field in fields if field.get("soil_moisture", 0) < 35)
        high_count = sum(1 for field in fields if field.get("soil_moisture", 0) > 70)
        if low_count > high_count:
            return "多块农田土壤偏干，建议优先补水，改善根区含水量。"
        if high_count > low_count:
            return "部分农田土壤偏湿，建议暂停灌溉并注意排水。"
        return "当前灌溉情况基本平衡，继续保持监测。"

    @staticmethod
    def get_summary() -> Dict[str, Any]:
        fields = field_store.all()
        total_fields = len(fields)
        total_area = sum(field.get("area", 0) for field in fields)
        average_area = total_area / total_fields if total_fields else 0
        average_moisture = sum(field.get("soil_moisture", 0) for field in fields) / total_fields if total_fields else 0
        average_temperature = sum(field.get("temperature", 0) for field in fields) / total_fields if total_fields else 0

        crop_types = {}
        for field in fields:
            crop_type = field.get("crop_type", "未知")
            crop_types[crop_type] = crop_types.get(crop_type, 0) + field.get("area", 0)

        return {
            "total_fields": total_fields,
            "total_area": total_area,
            "average_area": average_area,
            "average_moisture": average_moisture,
            "average_temperature": average_temperature,
            "crop_distribution": crop_types,
            "growth_prediction": AnalyticsModuleService._growth_prediction(fields),
            "estimated_yield": AnalyticsModuleService._estimated_yield(fields),
            "fertilizer_advice": AnalyticsModuleService._fertilizer_advice(fields),
            "irrigation_advice": AnalyticsModuleService._irrigation_advice(fields),
            "irrigation_recommendation": RuleEngine.evaluate_irrigation(fields),
            "pest_risk_warnings": RuleEngine.evaluate_pest_risk(fields),
            "trend_series": RuleEngine.build_trend_series(fields),
            "field_comparison": RuleEngine.build_field_comparison(fields),
        }
