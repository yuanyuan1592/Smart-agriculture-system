from fastapi import APIRouter
from typing import Any, Dict
from app.modules.analytics.service import AnalyticsModuleService

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_analytics_summary() -> Dict[str, Any]:
    return AnalyticsModuleService.get_summary()
