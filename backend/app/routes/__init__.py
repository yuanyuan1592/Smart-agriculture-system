from fastapi import APIRouter
from app.core.registry import register_module
from .field import router as field_router
from .detection import router as detection_router
from app.modules.analytics.routes import router as analytics_router

router = APIRouter()

router.include_router(field_router, prefix="/api/fields", tags=["fields"])
register_module("field", "/api/fields", ["fields"])

router.include_router(detection_router, prefix="/api/detection", tags=["detection"])
register_module("detection", "/api/detection", ["detection"])

router.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])
register_module("analytics", "/api/analytics", ["analytics"])

__all__ = ["router"]
