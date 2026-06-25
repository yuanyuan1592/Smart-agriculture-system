from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """项目统一配置入口，后续新增配置只需要在这里扩展。"""

    backend_root: Path = Path(__file__).resolve().parents[1]
    api_prefix: str = "/api"
    debug: bool = True


config = AppConfig()
