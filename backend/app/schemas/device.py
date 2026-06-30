from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DeviceBase(BaseModel):
    field_id: int
    name: str
    type: str
    type_name: str
    description: str
    status: str
    mode: str
    power_level: float


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    status: Optional[str] = None
    mode: Optional[str] = None
    power_level: Optional[float] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True
