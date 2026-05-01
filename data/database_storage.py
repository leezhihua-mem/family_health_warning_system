"""
数据存储模块
PostgreSQL时序数据库 + 用户健康档案存储

创建时间：2026-05-01 19:45
版本：v1.0
开发者：磐石Agent
"""

from datetime import datetime
from typing import Dict, List, Optional
import json

# ============================================
# 数据库表结构设计 ⭐⭐⭐⭐⭐
# ============================================

"""
数据库表结构：

1. users（用户表）⭐⭐⭐⭐⭐
   - user_id: 用户ID（主键）
   - username: 用户名
   - email: 邮箱
   - phone: 电话
   - age: 年龄
   - gender: 性别
   - health_status: 健康状态
   - created_at: 创建时间
   - updated_at: 更新时间

2. health_records（健康记录表）⭐⭐⭐⭐⭐
   - record_id: 记录ID（主键）
   - user_id: 用户ID（外键）
   - device_id: 设备ID
   - data_type: 数据类型
   - data_value: 数据值（JSON）
   - data_time: 数据时间
   - data_verified: 是否验证
   - created_at: 创建时间

3. warning_history（预警历史表）⭐⭐⭐⭐⭐
   - warning_id: 预警ID（主键）
   - user_id: 用户ID（外键）
   - warning_level: 预警等级
   - warning_type: 预警类型
   - explanation: 预警说明
   - suggestion: 建议措施（JSON）
   - validation_status: 验证状态
   - validation_score: 验证评分
   - warning_time: 预警时间
   - created_at: 创建时间

4. devices（设备表）
   - device_id: 设备ID（主键）
   - user_id: 用户ID（外键）
   - device_type: 设备类型
   - device_name: 设备名称
   - connect_status: 连接状态
   - last_data_time: 最后数据时间
   - created_at: 创建时间

5. notification_history（推送历史表）⭐⭐⭐⭐⭐
   - notification_id: 推送ID（主键）
   - warning_id: 预警ID（外键）
   - user_id: 用户ID（外键）
   - channel: 推送渠道
   - status: 推送状态
   - send_time: 推送时间
   - created_at: 创建时间
"""

# ============================================
# 数据库连接管理 ⭐⭐⭐⭐⭐
# ============================================

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_config: Optional[Dict] = None):
        self.name = "数据库管理器"
        self.db_config = db_config or {
            "host": "localhost",
            "port": 5432,
            "database": "family_health_warning",
            "user": "postgres",
            "password": "password"
        }
        self.connected = False
    
    def connect(self) -> bool:
        """连接数据库"""
        # 模拟数据库连接
        # 实际需要使用 psycopg2 或 SQLAlchemy
        self.connected = True
        return True
    
    def disconnect(self) -> bool:
        """断开数据库连接"""
        self.connected = False
        return True
    
    def is_connected(self) -> bool:
        """检查数据库连接状态"""
        return self.connected

# ============================================
# 用户档案存储 ⭐⭐⭐⭐⭐
# ============================================

class UserStorage:
    """用户档案存储"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.users_cache = {}  # 模拟缓存
    
    def create_user(
        self,
        user_id: str,
        username: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        health_status: Optional[str] = None
    ) -> Dict:
        """
        创建用户档案
        
        Args:
            user_id: 用户ID
            username: 用户名
            email: 邮箱
            phone: 电话
            age: 年龄
            gender: 性别
            health_status: 健康状态
        
        Returns:
            Dict: 用户档案
        """
        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "phone": phone,
            "age": age,
            "gender": gender,
            "health_status": health_status,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 存储到缓存（实际存储到PostgreSQL）
        self.users_cache[user_id] = user_data
        
        return user_data
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        获取用户档案
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[Dict]: 用户档案
        """
        return self.users_cache.get(user_id)
    
    def update_user(self, user_id: str, update_data: Dict) -> Optional[Dict]:
        """
        更新用户档案
        
        Args:
            user_id: 用户ID
            update_data: 更新数据
        
        Returns:
            Optional[Dict]: 更新后的用户档案
        """
        user_data = self.users_cache.get(user_id)
        if user_data:
            user_data.update(update_data)
            user_data["updated_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.users_cache[user_id] = user_data
            return user_data
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """
        删除用户档案
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 删除是否成功
        """
        if user_id in self.users_cache:
            del self.users_cache[user_id]
            return True
        return False

# ============================================
# 健康记录存储 ⭐⭐⭐⭐⭐
# ============================================

class HealthRecordStorage:
    """健康记录存储"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.records_cache = {}  # 模拟缓存
    
    def save_health_record(
        self,
        user_id: str,
        device_id: str,
        data_type: str,
        data_value: Dict,
        data_verified: bool = False
    ) -> Dict:
        """
        保存健康记录
        
        Args:
            user_id: 用户ID
            device_id: 设备ID
            data_type: 数据类型
            data_value: 数据值
            data_verified: 是否验证
        
        Returns:
            Dict: 健康记录
        """
        record_id = f"record_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        record_data = {
            "record_id": record_id,
            "user_id": user_id,
            "device_id": device_id,
            "data_type": data_type,
            "data_value": json.dumps(data_value),
            "data_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "data_verified": data_verified,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 存储到缓存（实际存储到PostgreSQL）
        self.records_cache[record_id] = record_data
        
        return record_data
    
    def get_user_health_records(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        获取用户健康记录
        
        Args:
            user_id: 用户ID
            limit: 限制数量
        
        Returns:
            List[Dict]: 健康记录列表
        """
        user_records = [
            r for r in self.records_cache.values()
            if r["user_id"] == user_id
        ]
        
        # 按时间排序
        user_records.sort(key=lambda x: x["data_time"], reverse=True)
        
        return user_records[:limit]
    
    def get_health_records_by_date(
        self,
        user_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict]:
        """
        获取指定日期范围内的健康记录
        
        Args:
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            List[Dict]: 健康记录列表
        """
        user_records = [
            r for r in self.records_cache.values()
            if r["user_id"] == user_id
            and start_date <= r["data_time"] <= end_date
        ]
        
        return user_records

# ============================================
# 预警历史存储 ⭐⭐⭐⭐⭐
# ============================================

class WarningHistoryStorage:
    """预警历史存储"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.warning_cache = {}  # 模拟缓存
    
    def save_warning_history(
        self,
        warning_id: str,
        user_id: str,
        warning_level: str,
        warning_type: str,
        explanation: str,
        suggestion: List[str],
        validation_status: str,
        validation_score: float
    ) -> Dict:
        """
        保存预警历史
        
        Args:
            warning_id: 预警ID
            user_id: 用户ID
            warning_level: 预警等级
            warning_type: 预警类型
            explanation: 预警说明
            suggestion: 建议措施
            validation_status: 验证状态
            validation_score: 验证评分
        
        Returns:
            Dict: 预警历史记录
        """
        warning_data = {
            "warning_id": warning_id,
            "user_id": user_id,
            "warning_level": warning_level,
            "warning_type": warning_type,
            "explanation": explanation,
            "suggestion": json.dumps(suggestion),
            "validation_status": validation_status,
            "validation_score": validation_score,
            "warning_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 存储到缓存（实际存储到PostgreSQL）
        self.warning_cache[warning_id] = warning_data
        
        return warning_data
    
    def get_user_warning_history(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        获取用户预警历史
        
        Args:
            user_id: 用户ID
            limit: 限制数量
        
        Returns:
            List[Dict]: 预警历史列表
        """
        user_warnings = [
            w for w in self.warning_cache.values()
            if w["user_id"] == user_id
        ]
        
        # 按时间排序
        user_warnings.sort(key=lambda x: x["warning_time"], reverse=True)
        
        return user_warnings[:limit]
    
    def get_warning_stats(self, user_id: str) -> Dict:
        """
        获取用户预警统计
        
        Args:
            user_id: 用户ID
        
        Returns:
            Dict: 预警统计
        """
        user_warnings = [
            w for w in self.warning_cache.values()
            if w["user_id"] == user_id
        ]
        
        # 统计各等级预警数量
        stats = {
            "total": len(user_warnings),
            "S_level": len([w for w in user_warnings if w["warning_level"] == "S"]),
            "A_level": len([w for w in user_warnings if w["warning_level"] == "A"]),
            "B_level": len([w for w in user_warnings if w["warning_level"] == "B"]),
            "C_level": len([w for w in user_warnings if w["warning_level"] == "C"])
        }
        
        return stats

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

def create_user_api(
    user_id: str,
    username: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    health_status: Optional[str] = None
) -> Dict:
    """创建用户API"""
    db_manager = DatabaseManager()
    db_manager.connect()
    
    user_storage = UserStorage(db_manager)
    result = user_storage.create_user(
        user_id, username, email, phone, age, gender, health_status
    )
    
    return result

def save_health_record_api(
    user_id: str,
    device_id: str,
    data_type: str,
    data_value: Dict,
    data_verified: bool = False
) -> Dict:
    """保存健康记录API"""
    db_manager = DatabaseManager()
    db_manager.connect()
    
    record_storage = HealthRecordStorage(db_manager)
    result = record_storage.save_health_record(
        user_id, device_id, data_type, data_value, data_verified
    )
    
    return result

def save_warning_history_api(
    warning_id: str,
    user_id: str,
    warning_level: str,
    warning_type: str,
    explanation: str,
    suggestion: List[str],
    validation_status: str,
    validation_score: float
) -> Dict:
    """保存预警历史API"""
    db_manager = DatabaseManager()
    db_manager.connect()
    
    warning_storage = WarningHistoryStorage(db_manager)
    result = warning_storage.save_warning_history(
        warning_id, user_id, warning_level, warning_type,
        explanation, suggestion, validation_status, validation_score
    )
    
    return result

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("数据存储模块测试")
    print("=" * 60)
    
    # 测试用户创建
    user_result = create_user_api(
        user_id="zhang_aunt_001",
        username="张阿姨",
        age=65,
        gender="女",
        health_status="糖尿病+高血压"
    )
    print(f"用户创建结果：{user_result}")
    
    # 测试健康记录保存
    record_result = save_health_record_api(
        user_id="zhang_aunt_001",
        device_id="BP_001",
        data_type="blood_pressure",
        data_value={"sbp_value": 135, "dbp_value": 88},
        data_verified=True
    )
    print(f"健康记录保存结果：{record_result}")
    
    # 测试预警历史保存
    warning_result = save_warning_history_api(
        warning_id="DKA_20260501_194500",
        user_id="zhang_aunt_001",
        warning_level="S",
        warning_type="酮症酸中毒联合预警",
        explanation="高血糖(15.0mmol/L) + 高血酮(3.5mmol/L)",
        suggestion=["立即就医", "补液治疗"],
        validation_status="pass",
        validation_score=100.0
    )
    print(f"预警历史保存结果：{warning_result}")
    
    print("=" * 60)