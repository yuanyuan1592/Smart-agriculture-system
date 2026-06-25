from typing import Any, Dict

from fastapi import APIRouter

from app.modules.detection.service import DetectionModuleService

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_detection_report():
    """获取农业检测报告。"""
    return DetectionModuleService.build_report()
