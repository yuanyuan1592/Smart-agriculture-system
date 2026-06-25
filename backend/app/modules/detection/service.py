from app.services.detection_service import build_detection_report
from app.services.field_service import field_store


class DetectionModuleService:
    """检测模块服务封装，作为模块级入口。"""

    @staticmethod
    def build_report():
        return build_detection_report(field_store.all())
