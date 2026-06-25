from fastapi import APIRouter
from .field import router as field_router

router = APIRouter()
router.include_router(field_router, prefix="/api/fields", tags=["fields"])

__all__ = ["router"]
