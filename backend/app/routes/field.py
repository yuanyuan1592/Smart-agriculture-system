from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import FieldCreate, FieldUpdate, FieldResponse
from app.modules.fields.service import FieldsModuleService

router = APIRouter()


@router.get("/", response_model=List[FieldResponse])
async def get_fields():
    """获取所有农田"""
    return FieldsModuleService.list_fields()


@router.get("/{field_id}", response_model=FieldResponse)
async def get_field(field_id: int):
    """获取特定农田"""
    field = FieldsModuleService.get_field(field_id)
    if field is None:
        raise HTTPException(status_code=404, detail="Farm field not found")
    return field


@router.post("/", response_model=FieldResponse)
async def create_field(field: FieldCreate):
    """创建农田"""
    return FieldsModuleService.create_field(field.model_dump())


@router.put("/{field_id}", response_model=FieldResponse)
async def update_field(field_id: int, field: FieldUpdate):
    """更新农田"""
    update_data = field.model_dump(exclude_unset=True)
    updated_field = FieldsModuleService.update_field(field_id, update_data)
    if updated_field is None:
        raise HTTPException(status_code=404, detail="Farm field not found")
    return updated_field


@router.delete("/{field_id}")
async def delete_field(field_id: int):
    """删除农田"""
    deleted = FieldsModuleService.delete_field(field_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Farm field not found")
    return {"message": "Field deleted successfully"}
