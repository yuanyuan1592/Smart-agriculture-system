from fastapi import APIRouter
from app.core.registry import register_module
from .field import router as field_router
from .detection import router as detection_router

router = APIRouter()

router.include_router(field_router, prefix="/api/fields", tags=["fields"])
register_module("field", "/api/fields", ["fields"])

router.include_router(detection_router, prefix="/api/detection", tags=["detection"])
register_module("detection", "/api/detection", ["detection"])

__all__ = ["router"]
