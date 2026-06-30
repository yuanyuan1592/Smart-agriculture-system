from app.common.device_store import device_store


class DevicesModuleService:
    """设备模块服务封装。"""

    @staticmethod
    def list_devices():
        return device_store.all()

    @staticmethod
    def list_devices_by_field(field_id: int):
        return device_store.list_by_field(field_id)

    @staticmethod
    def get_device(device_id: int):
        return device_store.get(device_id)

    @staticmethod
    def update_device(device_id: int, update_data: dict):
        return device_store.update(device_id, update_data)
