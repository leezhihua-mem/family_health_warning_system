"""
IoT数据接入模块
支持血压计、血糖仪、智能手表等设备数据接入

创建时间：2026-05-01 19:40
版本：v1.0
开发者：磐石Agent
"""

from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum

# ============================================
# 设备类型定义 ⭐⭐⭐⭐⭐
# ============================================

class DeviceType(Enum):
    """设备类型"""
    BLOOD_PRESSURE_MONITOR = "血压计"
    GLUCOSE_MONITOR = "血糖仪"
    KETONE_MONITOR = "血酮仪"
    SMART_WATCH = "智能手表"
    OXIMETER = "血氧仪"
    THERMOMETER = "体温计"
    WEIGHT_SCALE = "体重秤"
    HRV_MONITOR = "HRV监测仪"

# ============================================
# 设备数据结构 ⭐⭐⭐⭐⭐
# ============================================

class DeviceData:
    """设备数据结构"""
    device_id: str
    device_type: DeviceType
    user_id: str
    data_time: datetime
    data_value: Dict[str, float]
    data_verified: bool = False
    
    def __init__(
        self,
        device_id: str,
        device_type: DeviceType,
        user_id: str,
        data_time: datetime,
        data_value: Dict[str, float]
    ):
        self.device_id = device_id
        self.device_type = device_type
        self.user_id = user_id
        self.data_time = data_time
        self.data_value = data_value
        self.data_verified = False

# ============================================
# IoT数据接入接口 ⭐⭐⭐⭐⭐
# ============================================

class IoTDataIngestion:
    """IoT数据接入管理器"""
    
    def __init__(self):
        self.name = "IoT数据接入"
        self.connected_devices = []
    
    def connect_device(self, device_id: str, device_type: DeviceType) -> bool:
        """
        连接设备
        
        Args:
            device_id: 设备ID
            device_type: 设备类型
        
        Returns:
            bool: 连接是否成功
        """
        # 模拟设备连接
        device_info = {
            "device_id": device_id,
            "device_type": device_type.value,
            "connect_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "connected"
        }
        
        self.connected_devices.append(device_info)
        return True
    
    def receive_data(
        self,
        device_id: str,
        user_id: str,
        data_value: Dict[str, float]
    ) -> DeviceData:
        """
        接收设备数据
        
        Args:
            device_id: 设备ID
            user_id: 用户ID
            data_value: 数据值
        
        Returns:
            DeviceData: 设备数据对象
        """
        # 获取设备类型
        device_type = self._get_device_type(device_id)
        
        # 创建设备数据
        device_data = DeviceData(
            device_id=device_id,
            device_type=device_type,
            user_id=user_id,
            data_time=datetime.now(),
            data_value=data_value
        )
        
        # 数据验证
        device_data.data_verified = self._verify_data(device_data)
        
        return device_data
    
    def _get_device_type(self, device_id: str) -> DeviceType:
        """根据设备ID获取设备类型"""
        # 模拟设备类型识别
        if "BP" in device_id:
            return DeviceType.BLOOD_PRESSURE_MONITOR
        elif "GLU" in device_id:
            return DeviceType.GLUCOSE_MONITOR
        elif "KET" in device_id:
            return DeviceType.KETONE_MONITOR
        elif "WATCH" in device_id:
            return DeviceType.SMART_WATCH
        elif "OXI" in device_id:
            return DeviceType.OXIMETER
        elif "TEMP" in device_id:
            return DeviceType.THERMOMETER
        elif "WEIGHT" in device_id:
            return DeviceType.WEIGHT_SCALE
        elif "HRV" in device_id:
            return DeviceType.HRV_MONITOR
        else:
            return DeviceType.SMART_WATCH
    
    def _verify_data(self, device_data: DeviceData) -> bool:
        """数据验证"""
        # 基础验证逻辑
        if device_data.data_value is None:
            return False
        
        # 设备类型验证
        if device_data.device_type == DeviceType.BLOOD_PRESSURE_MONITOR:
            sbp = device_data.data_value.get("sbp_value")
            dbp = device_data.data_value.get("dbp_value")
            if sbp and dbp:
                if sbp < 60 or sbp > 250:
                    return False
                if dbp < 40 or dbp > 150:
                    return False
        elif device_data.device_type == DeviceType.GLUCOSE_MONITOR:
            glucose = device_data.data_value.get("glucose_value")
            if glucose:
                if glucose < 1.0 or glucose > 50.0:
                    return False
        
        return True
    
    def get_connected_devices(self) -> List[Dict]:
        """获取已连接设备列表"""
        return self.connected_devices
    
    def disconnect_device(self, device_id: str) -> bool:
        """断开设备连接"""
        for device in self.connected_devices:
            if device["device_id"] == device_id:
                device["status"] = "disconnected"
                return True
        return False

# ============================================
# 数据适配器（适配不同设备数据格式）⭐⭐⭐⭐⭐
# ============================================

class DataAdapter:
    """数据适配器"""
    
    @staticmethod
    def adapt_blood_pressure(raw_data: Dict) -> Dict[str, float]:
        """
        适配血压计数据
        
        Args:
            raw_data: 原始数据
        
        Returns:
            Dict: 适配后的数据
        """
        return {
            "sbp_value": raw_data.get("sbp", 0),
            "dbp_value": raw_data.get("dbp", 0)
        }
    
    @staticmethod
    def adapt_glucose(raw_data: Dict) -> Dict[str, float]:
        """
        适配血糖仪数据
        
        Args:
            raw_data: 原始数据
        
        Returns:
            Dict: 适配后的数据
        """
        return {
            "glucose_value": raw_data.get("glucose", 0)
        }
    
    @staticmethod
    def adapt_smart_watch(raw_data: Dict) -> Dict[str, float]:
        """
        适配智能手表数据
        
        Args:
            raw_data: 原始数据
        
        Returns:
            Dict: 适配后的数据
        """
        return {
            "heart_rate": raw_data.get("hr", 0),
            "hrv_value": raw_data.get("hrv", 0),
            "spo2_value": raw_data.get("spo2", 0)
        }

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

def connect_device_api(device_id: str, device_type: str) -> Dict:
    """
    连接设备API
    
    Args:
        device_id: 设备ID
        device_type: 设备类型
    
    Returns:
        Dict: 连接结果
    """
    ingestion = IoTDataIngestion()
    
    # 转换设备类型
    type_mapping = {
        "血压计": DeviceType.BLOOD_PRESSURE_MONITOR,
        "血糖仪": DeviceType.GLUCOSE_MONITOR,
        "血酮仪": DeviceType.KETONE_MONITOR,
        "智能手表": DeviceType.SMART_WATCH,
        "血氧仪": DeviceType.OXIMETER,
        "体温计": DeviceType.THERMOMETER,
        "体重秤": DeviceType.WEIGHT_SCALE,
        "HRV监测仪": DeviceType.HRV_MONITOR
    }
    
    device_type_enum = type_mapping.get(device_type, DeviceType.SMART_WATCH)
    
    result = ingestion.connect_device(device_id, device_type_enum)
    
    return {
        "success": result,
        "device_id": device_id,
        "device_type": device_type,
        "connect_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def receive_device_data_api(
    device_id: str,
    user_id: str,
    data_value: Dict[str, float]
) -> Dict:
    """
    接收设备数据API
    
    Args:
        device_id: 设备ID
        user_id: 用户ID
        data_value: 数据值
    
    Returns:
        Dict: 接收结果
    """
    ingestion = IoTDataIngestion()
    
    device_data = ingestion.receive_data(device_id, user_id, data_value)
    
    return {
        "success": True,
        "device_id": device_data.device_id,
        "device_type": device_data.device_type.value,
        "user_id": device_data.user_id,
        "data_time": device_data.data_time.strftime('%Y-%m-%d %H:%M:%S'),
        "data_value": device_data.data_value,
        "data_verified": device_data.data_verified
    }

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("IoT数据接入模块测试")
    print("=" * 60)
    
    # 测试连接设备
    result = connect_device_api("BP_001", "血压计")
    print(f"设备连接结果：{result}")
    
    # 测试接收数据
    data_result = receive_device_data_api(
        device_id="BP_001",
        user_id="zhang_aunt_001",
        data_value={"sbp_value": 135, "dbp_value": 88}
    )
    print(f"数据接收结果：{data_result}")
    
    print("=" * 60)