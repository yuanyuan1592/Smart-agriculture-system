from fastapi import APIRouter
from .field import router as field_router
from .detection import router as detection_router

router = APIRouter()
router.include_router(field_router, prefix="/api/fields", tags=["fields"])
router.include_router(detection_router, prefix="/api/detection", tags=["detection"])

__all__ = ["router"]
