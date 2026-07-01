from datetime import datetime
from typing import Any, Dict, List


class DeviceStore:
    """自动化设备存储服务，用于模拟设备状态和控制。"""

    def __init__(self) -> None:
        self._devices: List[Dict[str, Any]] = []
        self._initialize_mock_data()

    def _initialize_mock_data(self) -> None:
        mock_devices = [
            {
                "field_id": 1,
                "name": "北区灌溉系统",
                "type": "irrigation",
                "type_name": "灌溉系统",
                "description": "自动控制灌溉泵与喷灌阀门，保持土壤水分。",
                "status": "off",
                "mode": "auto",
                "power_level": 70,
            },
            {
                "field_id": 1,
                "name": "北区温度调节系统",
                "type": "temperature",
                "type_name": "温度调节系统",
                "description": "智能调节加热/制冷设备，稳定作物生长温度。",
                "status": "on",
                "mode": "auto",
                "power_level": 60,
            },
            {
                "field_id": 1,
                "name": "北区农药喷洒系统",
                "type": "pesticide",
                "type_name": "农药喷洒系统",
                "description": "按计划喷洒农药，可手动或自动模式控制。",
                "status": "off",
                "mode": "manual",
                "power_level": 40,
            },
            {
                "field_id": 1,
                "name": "北区通风系统",
                "type": "ventilation",
                "type_name": "通风系统",
                "description": "控制风机与通风口，改善空气流通。",
                "status": "on",
                "mode": "auto",
                "power_level": 80,
            },
            {
                "field_id": 2,
                "name": "东区灌溉系统",
                "type": "irrigation",
                "type_name": "灌溉系统",
                "description": "自动控制水泵与滴灌设备，为玉米提供稳定水分。",
                "status": "on",
                "mode": "auto",
                "power_level": 55,
            },
            {
                "field_id": 2,
                "name": "东区温度调节系统",
                "type": "temperature",
                "type_name": "温度调节系统",
                "description": "根据温度传感器动态调节加热和冷却装置。",
                "status": "off",
                "mode": "manual",
                "power_level": 50,
            },
            {
                "field_id": 2,
                "name": "东区农药喷洒系统",
                "type": "pesticide",
                "type_name": "农药喷洒系统",
                "description": "支持定时喷洒和立即执行的农药控制。",
                "status": "off",
                "mode": "auto",
                "power_level": 30,
            },
            {
                "field_id": 2,
                "name": "东区照明系统",
                "type": "lighting",
                "type_name": "补光照明系统",
                "description": "为作物提供补光，提升日照不足时光合作用效率。",
                "status": "on",
                "mode": "auto",
                "power_level": 75,
            },
            {
                "field_id": 3,
                "name": "南区灌溉系统",
                "type": "irrigation",
                "type_name": "灌溉系统",
                "description": "根据土壤湿度自动控制灌溉周期。",
                "status": "on",
                "mode": "auto",
                "power_level": 65,
            },
            {
                "field_id": 3,
                "name": "南区温度调节系统",
                "type": "temperature",
                "type_name": "温度调节系统",
                "description": "自动调节温室内温度，保障草莓生长环境。",
                "status": "on",
                "mode": "auto",
                "power_level": 45,
            },
            {
                "field_id": 3,
                "name": "南区农药喷洒系统",
                "type": "pesticide",
                "type_name": "农药喷洒系统",
                "description": "按虫害风险自动安排喷洒策略。",
                "status": "off",
                "mode": "manual",
                "power_level": 35,
            },
            {
                "field_id": 3,
                "name": "南区营养液系统",
                "type": "nutrient",
                "type_name": "营养液供应系统",
                "description": "精确供给营养液，提升作物生长健康。",
                "status": "on",
                "mode": "auto",
                "power_level": 50,
            },
            {
                "field_id": 4,
                "name": "西区灌溉系统",
                "type": "irrigation",
                "type_name": "灌溉系统",
                "description": "控制喷灌和滴灌设备，保证白菜土壤含水量。",
                "status": "off",
                "mode": "manual",
                "power_level": 60,
            },
            {
                "field_id": 4,
                "name": "西区温度调节系统",
                "type": "temperature",
                "type_name": "温度调节系统",
                "description": "冷暖结合的温度控制设备，支持自动调节。",
                "status": "on",
                "mode": "auto",
                "power_level": 70,
            },
            {
                "field_id": 4,
                "name": "西区农药喷洒系统",
                "type": "pesticide",
                "type_name": "农药喷洒系统",
                "description": "支持区域化喷洒和任务调度。",
                "status": "off",
                "mode": "auto",
                "power_level": 25,
            },
            {
                "field_id": 4,
                "name": "西区通风系统",
                "type": "ventilation",
                "type_name": "通风系统",
                "description": "维持空气流通，减少病菌滋生。",
                "status": "on",
                "mode": "auto",
                "power_level": 85,
            },
            {
                "field_id": 5,
                "name": "中区灌溉系统",
                "type": "irrigation",
                "type_name": "灌溉系统",
                "description": "根据土壤湿度自动调整浇水频率。",
                "status": "on",
                "mode": "auto",
                "power_level": 72,
            },
            {
                "field_id": 5,
                "name": "中区温度调节系统",
                "type": "temperature",
                "type_name": "温度调节系统",
                "description": "自动风冷与加热控制，保护辣椒生长。",
                "status": "off",
                "mode": "manual",
                "power_level": 55,
            },
            {
                "field_id": 5,
                "name": "中区农药喷洒系统",
                "type": "pesticide",
                "type_name": "农药喷洒系统",
                "description": "精准喷洒控制，减少药剂浪费。",
                "status": "off",
                "mode": "auto",
                "power_level": 30,
            },
            {
                "field_id": 5,
                "name": "中区照明系统",
                "type": "lighting",
                "type_name": "补光照明系统",
                "description": "夜间补光，增强植株光合作用。",
                "status": "on",
                "mode": "auto",
                "power_level": 58,
            },
            {
                "field_id": 6,
                "name": "温室灌溉系统",
                "type": "irrigation",
                "type_name": "灌溉系统",
                "description": "温室灌溉系统按湿度自动补水。",
                "status": "on",
                "mode": "auto",
                "power_level": 66,
            },
            {
                "field_id": 6,
                "name": "温室温度调节系统",
                "type": "temperature",
                "type_name": "温度调节系统",
                "description": "温室内恒温控制设备。",
                "status": "on",
                "mode": "auto",
                "power_level": 52,
            },
            {
                "field_id": 6,
                "name": "温室农药喷洒系统",
                "type": "pesticide",
                "type_name": "农药喷洒系统",
                "description": "温室内病虫害喷洒设备。",
                "status": "off",
                "mode": "manual",
                "power_level": 40,
            },
            {
                "field_id": 6,
                "name": "温室营养液系统",
                "type": "nutrient",
                "type_name": "营养液供应系统",
                "description": "为温室作物提供稳定营养液供应。",
                "status": "on",
                "mode": "auto",
                "power_level": 63,
            },
        ]

        for device in mock_devices:
            self.create(device)

    def _build_auto_control_message(self, device: Dict[str, Any], field_data: Dict[str, Any]) -> str | None:
        if not field_data or device.get("mode") != "auto":
            return None

        device_type = device.get("type")
        moisture = field_data.get("soil_moisture", 0)
        temperature = field_data.get("temperature", 0)
        light_intensity = field_data.get("light_intensity", 0)
        soil_ph = field_data.get("soil_ph", 0)
        moisture_low = field_data.get("moisture_threshold_low", 30.0)
        moisture_high = field_data.get("moisture_threshold_high", 70.0)
        temperature_high = field_data.get("temperature_threshold_high", 35.0)
        temperature_low = field_data.get("temperature_threshold_low", 15.0)
        light_low = field_data.get("light_threshold_low", 8000.0)
        light_high = field_data.get("light_threshold_high", 30000.0)
        ph_low = field_data.get("ph_threshold_low", 6.0)
        ph_high = field_data.get("ph_threshold_high", 7.5)

        if device_type == "irrigation":
            if moisture < moisture_low * 0.92:
                return "土壤偏干，自动启动灌溉"
            if moisture > moisture_high:
                return "土壤偏湿，自动停止灌溉"
        if device_type == "temperature":
            if temperature > temperature_high:
                return "温度偏高，自动启动降温"
            if temperature < temperature_low:
                return "温度偏低，自动启动保温"
        if device_type == "ventilation":
            if temperature > temperature_high or moisture > moisture_high:
                return "环境闷热，自动开启通风"
        if device_type == "lighting":
            if light_intensity < light_low * 0.85:
                return "光照不足，自动开启补光"
            if light_intensity > light_high * 0.95:
                return "光照过强，自动关闭补光"
        if device_type == "nutrient":
            if soil_ph < ph_low or soil_ph > ph_high:
                return "土壤酸碱度异常，自动调节营养液"
        return None

    def apply_auto_control_for_field(self, field_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not field_data:
            return []
        field_id = field_data.get("id")
        if field_id is None:
            return []

        field_devices = [device for device in self._devices if device.get("field_id") == field_id]
        for device in field_devices:
            message = self._build_auto_control_message(device, field_data)
            device["auto_control_message"] = message
            device["auto_control_active"] = bool(message)
            if not message:
                continue

            device_type = device.get("type")
            if device_type == "irrigation":
                device["status"] = "on" if "启动灌溉" in message else "off"
                device["power_level"] = 80 if device["status"] == "on" else 20
            elif device_type == "temperature":
                device["status"] = "on"
                device["power_level"] = 75 if "降温" in message else 65
            elif device_type == "ventilation":
                device["status"] = "on"
                device["power_level"] = 85
            elif device_type == "lighting":
                device["status"] = "on" if "开启补光" in message else "off"
                device["power_level"] = 80 if device["status"] == "on" else 10
            elif device_type == "nutrient":
                device["status"] = "on"
                device["power_level"] = 60

        return field_devices

    def all(self) -> List[Dict[str, Any]]:
        return list(self._devices)

    def get(self, device_id: int) -> Dict[str, Any] | None:
        return next((device for device in self._devices if device["id"] == device_id), None)

    def list_by_field(self, field_id: int) -> List[Dict[str, Any]]:
        return [device for device in self._devices if device["field_id"] == field_id]

    def create(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow()
        new_device = {
            "id": len(self._devices) + 1,
            "created_at": now,
            "updated_at": now,
            "last_updated": now,
            **device_data,
        }
        self._devices.append(new_device)
        return new_device

    def update(self, device_id: int, update_data: Dict[str, Any]) -> Dict[str, Any] | None:
        device = self.get(device_id)
        if not device:
            return None
        device.update(update_data)
        device["updated_at"] = datetime.utcnow()
        device["last_updated"] = device["updated_at"]
        return device


device_store = DeviceStore()
