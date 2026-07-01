from fastapi import APIRouter, Query
from typing import Any, Dict
from app.modules.analytics.service import AnalyticsModuleService

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_analytics_summary(days: int = Query(7, ge=1, le=30)) -> Dict[str, Any]:
    return AnalyticsModuleService.get_summary(days)
