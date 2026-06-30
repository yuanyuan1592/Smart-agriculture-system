from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import DeviceCreate, DeviceUpdate, DeviceResponse
from app.modules.devices.service import DevicesModuleService

router = APIRouter()


@router.get("/", response_model=List[DeviceResponse])
async def get_devices():
    return DevicesModuleService.list_devices()


@router.get("/field/{field_id}", response_model=List[DeviceResponse])
async def get_devices_by_field(field_id: int):
    return DevicesModuleService.list_devices_by_field(field_id)


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int):
    device = DevicesModuleService.get_device(device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, device: DeviceUpdate):
    updated_device = DevicesModuleService.update_device(device_id, device.model_dump(exclude_unset=True))
    if updated_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device
