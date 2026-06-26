from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FieldCreate(BaseModel):
    """创建农田请求"""
    name: str
    location: str
    area: float
    crop_type: str
    soil_moisture: float
    temperature: float


class FieldUpdate(BaseModel):
    """更新农田请求"""
    name: Optional[str] = None
    location: Optional[str] = None
    area: Optional[float] = None
    crop_type: Optional[str] = None
    soil_moisture: Optional[float] = None
    temperature: Optional[float] = None


class FieldResponse(BaseModel):
    """农田响应"""
    id: int
    name: str
    location: str
    area: float
    crop_type: str
    soil_moisture: float
    temperature: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
