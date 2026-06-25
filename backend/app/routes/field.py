from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import FieldCreate, FieldUpdate, FieldResponse

router = APIRouter()

# 临时存储数据（实际应使用数据库）
fields_db = []


@router.get("/", response_model=List[FieldResponse])
async def get_fields():
    """获取所有农田"""
    return fields_db


@router.get("/{field_id}", response_model=FieldResponse)
async def get_field(field_id: int):
    """获取特定农田"""
    for field in fields_db:
        if field.get("id") == field_id:
            return field
    raise HTTPException(status_code=404, detail="Farm field not found")


@router.post("/", response_model=FieldResponse)
async def create_field(field: FieldCreate):
    """创建农田"""
    new_field = {
        "id": len(fields_db) + 1,
        **field.model_dump()
    }
    fields_db.append(new_field)
    return new_field


@router.put("/{field_id}", response_model=FieldResponse)
async def update_field(field_id: int, field: FieldUpdate):
    """更新农田"""
    for idx, f in enumerate(fields_db):
        if f.get("id") == field_id:
            update_data = field.model_dump(exclude_unset=True)
            fields_db[idx].update(update_data)
            return fields_db[idx]
    raise HTTPException(status_code=404, detail="Farm field not found")


@router.delete("/{field_id}")
async def delete_field(field_id: int):
    """删除农田"""
    for idx, f in enumerate(fields_db):
        if f.get("id") == field_id:
            fields_db.pop(idx)
            return {"message": "Field deleted successfully"}
    raise HTTPException(status_code=404, detail="Farm field not found")
