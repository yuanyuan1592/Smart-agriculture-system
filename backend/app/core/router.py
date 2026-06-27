from fastapi import APIRouter, FastAPI
from app.modules.fields.routes import router as fields_router
from app.modules.detection.routes import router as detection_router
from app.modules.analytics.routes import router as analytics_router
from app.modules.weather.routes import router as weather_router


def register_routes(app: FastAPI) -> None:
    """注册所有模块路由到主应用。"""
    api_router = APIRouter(prefix="/api")

    api_router.include_router(fields_router, prefix="/fields", tags=["fields"])
    api_router.include_router(detection_router, prefix="/detection", tags=["detection"])
    api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
    api_router.include_router(weather_router, prefix="/weather", tags=["weather"])

    app.include_router(api_router)
