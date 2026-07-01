from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from app.modules.farm.service import FarmModuleService

router = APIRouter()


@router.get("/tasks", response_model=List[Dict[str, Any]])
async def get_tasks():
    return FarmModuleService.list_tasks()


@router.post("/tasks", response_model=Dict[str, Any])
async def create_task(payload: Dict[str, Any]):
    return FarmModuleService.create_task(payload)


@router.put("/tasks/{task_id}", response_model=Dict[str, Any])
async def update_task(task_id: int, payload: Dict[str, Any]):
    try:
        return FarmModuleService.update_task(task_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/tasks/{task_id}/complete", response_model=Dict[str, Any])
async def complete_task(task_id: int):
    try:
        return FarmModuleService.complete_task(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/tasks/{task_id}", response_model=Dict[str, Any])
async def delete_task(task_id: int):
    try:
        return FarmModuleService.delete_task(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/growth-stages", response_model=List[Dict[str, Any]])
async def get_growth_stages():
    return FarmModuleService.get_growth_stages()


@router.get("/faults", response_model=List[Dict[str, Any]])
async def get_faults():
    return FarmModuleService.get_faults()


@router.get("/summary", response_model=Dict[str, Any])
async def get_summary():
    return FarmModuleService.get_farm_summary()


@router.get("/report", response_model=Dict[str, Any])
async def get_report():
    from app.common.weather_store import weather_store

    tasks = FarmModuleService.list_tasks()
    faults = FarmModuleService.get_faults()
    weather_items = weather_store.all()
    return FarmModuleService.get_operational_report(tasks=tasks, faults=faults, weather_items=weather_items)


@router.get("/alerts", response_model=List[Dict[str, Any]])
async def get_alerts():
    from app.common.weather_store import weather_store

    tasks = FarmModuleService.list_tasks()
    faults = FarmModuleService.get_faults()
    weather_items = weather_store.all()
    return FarmModuleService.get_operational_alerts(tasks=tasks, faults=faults, weather_items=weather_items)
