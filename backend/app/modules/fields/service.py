from app.common.field_store import field_store


class FieldsModuleService:
    """字段模块服务封装，作为模块级入口。"""

    @staticmethod
    def list_fields():
        return field_store.all()

    @staticmethod
    def get_field(field_id: int):
        return field_store.get(field_id)

    @staticmethod
    def create_field(field_data: dict):
        return field_store.create(field_data)

    @staticmethod
    def update_field(field_id: int, field_data: dict):
        return field_store.update(field_id, field_data)

    @staticmethod
    def delete_field(field_id: int):
        return field_store.delete(field_id)
