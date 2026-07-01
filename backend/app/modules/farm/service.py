from app.common.field_store import field_store
from app.common.device_store import device_store
from datetime import datetime, timedelta
from typing import Any, Dict, List


class FarmModuleService:
    _tasks: List[Dict[str, Any]] = []

    @staticmethod
    def _bootstrap_tasks() -> List[Dict[str, Any]]:
        if FarmModuleService._tasks:
            return FarmModuleService._tasks

        FarmModuleService._tasks = [
            {
                "id": 1,
                "field_id": 1,
                "field_name": "北区番茄田",
                "task_type": "浇水",
                "title": "补水灌溉",
                "description": "上午进行灌溉，维持土壤湿度稳定",
                "status": "已完成",
                "scheduled_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            },
            {
                "id": 2,
                "field_id": 2,
                "field_name": "东区玉米田",
                "task_type": "施肥",
                "title": "追肥作业",
                "description": "根据土壤检测结果进行氮肥追施",
                "status": "进行中",
                "scheduled_at": datetime.utcnow().isoformat(),
            },
            {
                "id": 3,
                "field_id": 3,
                "field_name": "南区草莓园",
                "task_type": "喷药",
                "title": "病虫害防治",
                "description": "针对低温潮湿天气进行预防性喷药",
                "status": "待执行",
                "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            },
            {
                "id": 4,
                "field_id": 4,
                "field_name": "西区白菜田",
                "task_type": "采收",
                "title": "白菜采收",
                "description": "根据成熟度进行采收",
                "status": "待执行",
                "scheduled_at": (datetime.utcnow() + timedelta(days=2)).isoformat(),
            },
        ]
        return FarmModuleService._tasks

    @staticmethod
    def reset_tasks() -> None:
        FarmModuleService._tasks = []

    @staticmethod
    def list_tasks() -> List[Dict[str, Any]]:
        return FarmModuleService._bootstrap_tasks()

    @staticmethod
    def create_task(payload: Dict[str, Any]) -> Dict[str, Any]:
        tasks = FarmModuleService._bootstrap_tasks()
        task = {
            "id": max((task["id"] for task in tasks), default=0) + 1,
            "field_id": payload.get("field_id", 1),
            "field_name": payload.get("field_name", "默认农田"),
            "task_type": payload.get("task_type", "常规"),
            "title": payload.get("title", "新任务"),
            "description": payload.get("description", ""),
            "status": payload.get("status", "待执行"),
            "scheduled_at": payload.get("scheduled_at") or datetime.utcnow().isoformat(),
        }
        tasks.append(task)
        return task

    @staticmethod
    def update_task(task_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        tasks = FarmModuleService._bootstrap_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task.update(payload)
                return task
        raise ValueError("task not found")

    @staticmethod
    def complete_task(task_id: int) -> Dict[str, Any]:
        return FarmModuleService.update_task(task_id, {"status": "已完成"})

    @staticmethod
    def delete_task(task_id: int) -> Dict[str, Any]:
        tasks = FarmModuleService._bootstrap_tasks()
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                removed = tasks.pop(index)
                return removed
        raise ValueError("task not found")

    @staticmethod
    def get_growth_stages() -> List[Dict[str, Any]]:
        return [
            {
                "crop_type": "番茄",
                "stage": "播种",
                "progress": 25,
                "description": "幼苗期，需保证温度和湿度稳定",
            },
            {
                "crop_type": "番茄",
                "stage": "生长",
                "progress": 65,
                "description": "开花结果期，需关注光照与肥水",
            },
            {
                "crop_type": "番茄",
                "stage": "授粉",
                "progress": 80,
                "description": "授粉期，注意温湿环境",
            },
            {
                "crop_type": "番茄",
                "stage": "采收",
                "progress": 90,
                "description": "成熟采收期，及时采收",
            },
            {
                "crop_type": "玉米",
                "stage": "播种",
                "progress": 20,
                "description": "玉米播种后管理",
            },
            {
                "crop_type": "玉米",
                "stage": "生长",
                "progress": 55,
                "description": "苗期生长，注重水肥平衡",
            },
            {
                "crop_type": "玉米",
                "stage": "授粉",
                "progress": 70,
                "description": "授粉期管理",
            },
            {
                "crop_type": "玉米",
                "stage": "采收",
                "progress": 85,
                "description": "成熟收获期",
            },
        ]

    @staticmethod
    def get_faults() -> List[Dict[str, Any]]:
        faults = []
        for device in device_store.all():
            if device.get("status") == "off" and device.get("type") in {"irrigation", "lighting", "temperature"}:
                faults.append({
                    "id": device["id"],
                    "device_name": device["name"],
                    "device_type": device["type_name"],
                    "fault": "设备异常",
                    "message": "设备已停止运行，请检查电源、传感器或控制模块",
                    "field_id": device.get("field_id"),
                })
        return faults

    @staticmethod
    def get_operational_alerts(
        tasks: List[Dict[str, Any]] | None = None,
        faults: List[Dict[str, Any]] | None = None,
        weather_items: List[Dict[str, Any]] | None = None,
    ) -> List[Dict[str, Any]]:
        task_items = tasks or FarmModuleService.list_tasks()
        fault_items = faults or FarmModuleService.get_faults()
        weather_data = weather_items or []

        alerts: List[Dict[str, Any]] = []

        for task in task_items:
            if task.get("status") != "已完成":
                alerts.append(
                    {
                        "id": f"task-{task['id']}",
                        "task_id": task["id"],
                        "type": "task_reminder",
                        "title": f"任务提醒：{task.get('title', '未命名任务')}",
                        "message": f"当前任务仍在{task.get('status', '待执行')}，请及时安排执行。",
                    }
                )

        for fault in fault_items:
            alerts.append(
                {
                    "id": f"fault-{fault.get('id', 'unknown')}",
                    "type": "device_fault",
                    "title": "设备故障提醒",
                    "message": f"{fault.get('device_name', '设备')}出现异常：{fault.get('message', '请检查')}",
                }
            )

        for weather_item in weather_data:
            predictions = weather_item.get("disaster_predictions", [])
            if predictions:
                alerts.append(
                    {
                        "id": f"weather-{weather_item.get('id', 'unknown')}",
                        "type": "weather_warning",
                        "title": f"天气预警：{weather_item.get('location', '当前区域')}",
                        "message": " · ".join(predictions),
                    }
                )

        return alerts

    @staticmethod
    def get_operational_report(
        tasks: List[Dict[str, Any]] | None = None,
        faults: List[Dict[str, Any]] | None = None,
        weather_items: List[Dict[str, Any]] | None = None,
    ) -> Dict[str, Any]:
        task_items = tasks or FarmModuleService.list_tasks()
        fault_items = faults or FarmModuleService.get_faults()
        weather_data = weather_items or []
        pending_tasks = sum(1 for task in task_items if task.get("status") == "待执行")
        completed_tasks = sum(1 for task in task_items if task.get("status") == "已完成")
        weather_warning_count = sum(1 for item in weather_data if item.get("disaster_predictions"))

        recommendations: List[str] = []
        if pending_tasks:
            recommendations.append(f"优先处理 {pending_tasks} 项待执行任务，避免影响农事节奏。")
        if fault_items:
            recommendations.append("检查设备故障，优先恢复灌溉、照明或温控设备。")
        if weather_warning_count:
            recommendations.append("根据天气预警调整施肥、喷药和采收安排。")
        if not recommendations:
            recommendations.append("当前农事节奏稳定，建议继续保持现有管理节奏。")

        return {
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "fault_count": len(fault_items),
            "weather_warning_count": weather_warning_count,
            "recommendations": recommendations,
        }

    @staticmethod
    def get_farm_summary() -> Dict[str, Any]:
        fields = field_store.all()
        tasks = FarmModuleService.list_tasks()
        faults = FarmModuleService.get_faults()
        return {
            "total_fields": len(fields),
            "active_tasks": sum(1 for task in tasks if task["status"] == "进行中"),
            "pending_tasks": sum(1 for task in tasks if task["status"] == "待执行"),
            "fault_count": len(faults),
            "recent_tasks": tasks[:3],
        }
