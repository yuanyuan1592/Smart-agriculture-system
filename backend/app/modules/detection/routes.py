from fastapi import APIRouter
from typing import Any, Dict
from app.modules.detection.service import DetectionModuleService

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_detection_report():
    return DetectionModuleService.build_report()
