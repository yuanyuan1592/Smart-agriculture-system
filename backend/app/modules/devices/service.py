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

    @staticmethod
    def auto_control_for_field(field_id: int):
        field = None
        from app.common.field_store import field_store

        for item in field_store.all():
            if item.get("id") == field_id:
                field = item
                break
        if field is None:
            return []
        return device_store.apply_auto_control_for_field(field)
