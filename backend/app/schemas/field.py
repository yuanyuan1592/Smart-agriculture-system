from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class FieldHistoryItem(BaseModel):
    timestamp: datetime
    soil_moisture: float
    temperature: float


class FieldCreate(BaseModel):
    """创建农田请求"""
    name: str
    location: str
    area: float
    crop_type: str
    soil_moisture: float
    temperature: float
    moisture_threshold_low: Optional[float] = None
    moisture_threshold_high: Optional[float] = None
    temperature_threshold_low: Optional[float] = None
    temperature_threshold_high: Optional[float] = None


class FieldUpdate(BaseModel):
    """更新农田请求"""
    name: Optional[str] = None
    location: Optional[str] = None
    area: Optional[float] = None
    crop_type: Optional[str] = None
    soil_moisture: Optional[float] = None
    temperature: Optional[float] = None
    moisture_threshold_low: Optional[float] = None
    moisture_threshold_high: Optional[float] = None
    temperature_threshold_low: Optional[float] = None
    temperature_threshold_high: Optional[float] = None


class FieldResponse(BaseModel):
    """农田响应"""
    id: int
    name: str
    location: str
    area: float
    crop_type: str
    soil_moisture: float
    temperature: float
    moisture_threshold_low: float
    moisture_threshold_high: float
    temperature_threshold_low: float
    temperature_threshold_high: float
    last_measurement_at: datetime
    history: List[FieldHistoryItem]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
