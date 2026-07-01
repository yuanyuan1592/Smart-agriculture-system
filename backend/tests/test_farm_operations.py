import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.modules.farm.service import FarmModuleService


def test_create_update_complete_and_delete_task_flow():
    FarmModuleService.reset_tasks()

    created = FarmModuleService.create_task(
        {
            "field_name": "北区番茄田",
            "task_type": "浇水",
            "title": "晨间补水",
            "description": "为幼苗补水",
            "status": "待执行",
            "scheduled_at": "2026-07-01T09:00:00",
        }
    )

    assert created["id"] is not None
    assert created["title"] == "晨间补水"
    assert created["scheduled_at"] == "2026-07-01T09:00:00"

    updated = FarmModuleService.update_task(
        created["id"],
        {
            "title": "午间补水",
            "description": "为幼苗补水并检查土壤湿度",
            "status": "进行中",
            "scheduled_at": "2026-07-02T10:00:00",
        },
    )

    assert updated["title"] == "午间补水"
    assert updated["status"] == "进行中"
    assert updated["scheduled_at"] == "2026-07-02T10:00:00"

    completed = FarmModuleService.complete_task(created["id"])
    assert completed["status"] == "已完成"

    deleted = FarmModuleService.delete_task(created["id"])
    assert deleted["id"] == created["id"]

    tasks = FarmModuleService.list_tasks()
    assert all(task["id"] != created["id"] for task in tasks)


def test_get_operational_alerts_links_task_with_weather_and_faults():
    alerts = FarmModuleService.get_operational_alerts(
        tasks=[{"id": 1, "title": "浇水", "task_type": "浇水", "status": "待执行"}],
        faults=[{"device_name": "灌溉泵", "message": "设备已停止运行"}],
        weather_items=[{"location": "北园区", "disaster_predictions": ["高温预警", "干旱预警"]}],
    )

    assert any(alert["type"] == "device_fault" for alert in alerts)
    assert any(alert["type"] == "weather_warning" for alert in alerts)
    assert any(alert["task_id"] == 1 for alert in alerts)


def test_get_operational_report_generates_recommendations():
    report = FarmModuleService.get_operational_report(
        tasks=[{"id": 1, "title": "浇水", "status": "待执行"}, {"id": 2, "title": "施肥", "status": "已完成"}],
        faults=[{"device_name": "灌溉泵", "message": "设备已停止运行"}],
        weather_items=[{"location": "北园区", "disaster_predictions": ["高温预警"]}],
    )

    assert report["pending_tasks"] == 1
    assert report["fault_count"] == 1
    assert any("设备故障" in item for item in report["recommendations"])
