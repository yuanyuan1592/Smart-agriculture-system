from typing import List, Tuple


class ModuleRegistry:
    """统一管理各功能模块的路由注册信息。"""

    def __init__(self) -> None:
        self._routes: List[Tuple[str, str, str]] = []

    def register(self, module_name: str, prefix: str, tags: List[str] | None = None) -> None:
        self._routes.append((module_name, prefix, ",".join(tags or [])))

    def all(self) -> List[Tuple[str, str, str]]:
        return list(self._routes)


registry = ModuleRegistry()


def register_module(module_name: str, prefix: str, tags: List[str] | None = None) -> None:
    registry.register(module_name, prefix, tags)


def get_registered_routes() -> List[Tuple[str, str, str]]:
    return registry.all()
