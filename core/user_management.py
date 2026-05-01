"""
用户管理模块
用户档案 + 权限控制 + 家庭成员管理

创建时间：2026-05-01 22:06
版本：v1.0
开发者：磐石Agent + 枢衡Agent
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

# ============================================
# 用户角色定义 ⭐⭐⭐⭐⭐
# ============================================

class UserRole(Enum):
    """用户角色"""
    ADMIN = "admin"  # 系统管理员 ⭐⭐⭐⭐⭐
    FAMILY_ADMIN = "family_admin"  # 家庭管理员 ⭐⭐⭐⭐⭐
    FAMILY_MEMBER = "family_member"  # 家庭成员 ⭐⭐⭐⭐⭐
    MEDICAL_STAFF = "medical_staff"  # 医疗人员 ⭐⭐⭐⭐⭐
    PATIENT = "patient"  # 患者 ⭐⭐⭐⭐⭐

# ============================================
# 权限定义 ⭐⭐⭐⭐⭐
# ============================================

class Permission(Enum):
    """权限定义"""
    # 基础权限
    VIEW_OWN_DATA = "view_own_data"  # 查看自己数据 ⭐⭐⭐⭐⭐
    EDIT_OWN_DATA = "edit_own_data"  # 编辑自己数据 ⭐⭐⭐⭐⭐
    
    # 家庭权限
    VIEW_FAMILY_DATA = "view_family_data"  # 查看家庭数据 ⭐⭐⭐⭐⭐
    EDIT_FAMILY_DATA = "edit_family_data"  # 编辑家庭数据 ⭐⭐⭐⭐⭐
    MANAGE_FAMILY_MEMBERS = "manage_family_members"  # 管理家庭成员 ⭐⭐⭐⭐⭐
    VIEW_FAMILY_WARNINGS = "view_family_warnings"  # 查看家庭预警 ⭐⭐⭐⭐⭐
    RECEIVE_FAMILY_NOTIFICATIONS = "receive_family_notifications"  # 接收家庭通知 ⭐⭐⭐⭐⭐
    
    # 医疗权限
    VIEW_PATIENT_DATA = "view_patient_data"  # 查看患者数据 ⭐⭐⭐⭐⭐
    EDIT_PATIENT_DATA = "edit_patient_data"  # 编辑患者数据 ⭐⭐⭐⭐⭐
    VIEW_PATIENT_WARNINGS = "view_patient_warnings"  # 查看患者预警 ⭐⭐⭐⭐⭐
    SEND_MEDICAL_NOTIFICATIONS = "send_medical_notifications"  # 发送医疗通知 ⭐⭐⭐⭐⭐
    ACCESS_MEDICAL_DASHBOARD = "access_medical_dashboard"  # 医疗仪表板 ⭐⭐⭐⭐⭐
    
    # 系统权限
    MANAGE_USERS = "manage_users"  # 管理用户 ⭐⭐⭐⭐⭐
    MANAGE_DEVICES = "manage_devices"  # 管理设备 ⭐⭐⭐⭐⭐
    SYSTEM_CONFIG = "system_config"  # 系统配置 ⭐⭐⭐⭐⭐

# ============================================
# 角色权限映射 ⭐⭐⭐⭐⭐
# ============================================

ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        Permission.VIEW_OWN_DATA,
        Permission.EDIT_OWN_DATA,
        Permission.VIEW_FAMILY_DATA,
        Permission.EDIT_FAMILY_DATA,
        Permission.MANAGE_FAMILY_MEMBERS,
        Permission.VIEW_FAMILY_WARNINGS,
        Permission.RECEIVE_FAMILY_NOTIFICATIONS,
        Permission.MANAGE_USERS,
        Permission.MANAGE_DEVICES,
        Permission.SYSTEM_CONFIG,
    ],
    UserRole.FAMILY_ADMIN: [
        Permission.VIEW_OWN_DATA,
        Permission.EDIT_OWN_DATA,
        Permission.VIEW_FAMILY_DATA,
        Permission.EDIT_FAMILY_DATA,
        Permission.MANAGE_FAMILY_MEMBERS,
        Permission.VIEW_FAMILY_WARNINGS,
        Permission.RECEIVE_FAMILY_NOTIFICATIONS,
    ],
    UserRole.FAMILY_MEMBER: [
        Permission.VIEW_OWN_DATA,
        Permission.EDIT_OWN_DATA,
        Permission.VIEW_FAMILY_DATA,
        Permission.VIEW_FAMILY_WARNINGS,
        Permission.RECEIVE_FAMILY_NOTIFICATIONS,
    ],
    UserRole.MEDICAL_STAFF: [
        Permission.VIEW_PATIENT_DATA,
        Permission.EDIT_PATIENT_DATA,
        Permission.VIEW_PATIENT_WARNINGS,
        Permission.SEND_MEDICAL_NOTIFICATIONS,
        Permission.ACCESS_MEDICAL_DASHBOARD,
    ],
    UserRole.PATIENT: [
        Permission.VIEW_OWN_DATA,
        Permission.EDIT_OWN_DATA,
    ],
}

# ============================================
# 用户档案结构 ⭐⭐⭐⭐⭐
# ============================================

class UserProfile:
    """用户档案"""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        role: UserRole,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        health_status: Optional[str] = None,
        family_id: Optional[str] = None,
        medical_id: Optional[str] = None,
    ):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.email = email
        self.phone = phone
        self.age = age
        self.gender = gender
        self.health_status = health_status
        self.family_id = family_id  # 家庭ID ⭐⭐⭐⭐⭐
        self.medical_id = medical_id  # 医疗机构ID
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.is_active = True
    
    def has_permission(self, permission: Permission) -> bool:
        """检查用户是否有某个权限"""
        return permission in ROLE_PERMISSIONS.get(self.role, [])
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role.value,
            "email": self.email,
            "phone": self.phone,
            "age": self.age,
            "gender": self.gender,
            "health_status": self.health_status,
            "family_id": self.family_id,
            "medical_id": self.medical_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }

# ============================================
# 家庭管理 ⭐⭐⭐⭐⭐
# ============================================

class FamilyManager:
    """家庭管理器"""
    
    def __init__(self):
        self.families = {}  # 家庭ID -> 家庭信息
        self.family_members = {}  # 家庭ID -> 成员列表
    
    def create_family(
        self,
        family_id: str,
        family_name: str,
        admin_user_id: str,
    ) -> Dict:
        """
        创建家庭
        
        Args:
            family_id: 家庭ID
            family_name: 家庭名称
            admin_user_id: 家庭管理员ID
        
        Returns:
            Dict: 家庭信息
        """
        family_data = {
            "family_id": family_id,
            "family_name": family_name,
            "admin_user_id": admin_user_id,
            "members": [admin_user_id],
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        self.families[family_id] = family_data
        self.family_members[family_id] = [admin_user_id]
        
        return family_data
    
    def add_family_member(
        self,
        family_id: str,
        user_id: str,
    ) -> bool:
        """
        添加家庭成员
        
        Args:
            family_id: 家庭ID
            user_id: 用户ID
        
        Returns:
            bool: 添加是否成功
        """
        if family_id not in self.families:
            return False
        
        if user_id not in self.family_members[family_id]:
            self.family_members[family_id].append(user_id)
            self.families[family_id]["members"] = self.family_members[family_id]
            self.families[family_id]["updated_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return True
    
    def remove_family_member(
        self,
        family_id: str,
        user_id: str,
    ) -> bool:
        """
        移除家庭成员
        
        Args:
            family_id: 家庭ID
            user_id: 用户ID
        
        Returns:
            bool: 移除是否成功
        """
        if family_id not in self.families:
            return False
        
        if user_id in self.family_members[family_id]:
            self.family_members[family_id].remove(user_id)
            self.families[family_id]["members"] = self.family_members[family_id]
            self.families[family_id]["updated_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return True
    
    def get_family_members(self, family_id: str) -> List[str]:
        """
        获取家庭成员列表
        
        Args:
            family_id: 家庭ID
        
        Returns:
            List[str]: 成员ID列表
        """
        return self.family_members.get(family_id, [])
    
    def get_family_info(self, family_id: str) -> Optional[Dict]:
        """
        获取家庭信息
        
        Args:
            family_id: 家庭ID
        
        Returns:
            Optional[Dict]: 家庭信息
        """
        return self.families.get(family_id)

# ============================================
# 用户管理器 ⭐⭐⭐⭐⭐
# ============================================

class UserManager:
    """用户管理器"""
    
    def __init__(self):
        self.users = {}  # 用户ID -> 用户档案
        self.family_manager = FamilyManager()
    
    def create_user(
        self,
        user_id: str,
        username: str,
        role: UserRole,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        age: Optional[int] = None,
        gender: Optional[str] = None,
        health_status: Optional[str] = None,
        family_id: Optional[str] = None,
        medical_id: Optional[str] = None,
    ) -> UserProfile:
        """
        创建用户
        
        Args:
            user_id: 用户ID
            username: 用户名
            role: 用户角色
            email: 邮箱
            phone: 电话
            age: 年龄
            gender: 性别
            health_status: 健康状态
            family_id: 家庭ID
            medical_id: 医疗机构ID
        
        Returns:
            UserProfile: 用户档案
        """
        user_profile = UserProfile(
            user_id=user_id,
            username=username,
            role=role,
            email=email,
            phone=phone,
            age=age,
            gender=gender,
            health_status=health_status,
            family_id=family_id,
            medical_id=medical_id,
        )
        
        self.users[user_id] = user_profile
        
        # 如果是家庭管理员，添加到家庭
        if family_id and role == UserRole.FAMILY_ADMIN:
            self.family_manager.add_family_member(family_id, user_id)
        
        return user_profile
    
    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """
        获取用户档案
        
        Args:
            user_id: 用户ID
        
        Returns:
            Optional[UserProfile]: 用户档案
        """
        return self.users.get(user_id)
    
    def update_user(
        self,
        user_id: str,
        update_data: Dict,
    ) -> Optional[UserProfile]:
        """
        更新用户档案
        
        Args:
            user_id: 用户ID
            update_data: 更新数据
        
        Returns:
            Optional[UserProfile]: 更新后的用户档案
        """
        user_profile = self.users.get(user_id)
        if user_profile:
            # 更新字段
            for key, value in update_data.items():
                if hasattr(user_profile, key):
                    setattr(user_profile, key, value)
            
            user_profile.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return user_profile
        
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            bool: 删除是否成功
        """
        if user_id in self.users:
            user_profile = self.users[user_id]
            
            # 如果用户属于家庭，从家庭中移除
            if user_profile.family_id:
                self.family_manager.remove_family_member(
                    user_profile.family_id, user_id
                )
            
            del self.users[user_id]
            return True
        
        return False
    
    def check_permission(
        self,
        user_id: str,
        permission: Permission,
    ) -> bool:
        """
        检查用户权限
        
        Args:
            user_id: 用户ID
            permission: 权限
        
        Returns:
            bool: 是否有权限
        """
        user_profile = self.users.get(user_id)
        if user_profile:
            return user_profile.has_permission(permission)
        
        return False
    
    def get_family_users(self, family_id: str) -> List[UserProfile]:
        """
        获取家庭所有用户
        
        Args:
            family_id: 家庭ID
        
        Returns:
            List[UserProfile]: 用户列表
        """
        member_ids = self.family_manager.get_family_members(family_id)
        
        return [
            self.users.get(user_id)
            for user_id in member_ids
            if self.users.get(user_id)
        ]

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

def create_user_api(
    user_id: str,
    username: str,
    role: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    health_status: Optional[str] = None,
    family_id: Optional[str] = None,
    medical_id: Optional[str] = None,
) -> Dict:
    """创建用户API"""
    manager = UserManager()
    
    # 转换角色
    role_mapping = {
        "admin": UserRole.ADMIN,
        "family_admin": UserRole.FAMILY_ADMIN,
        "family_member": UserRole.FAMILY_MEMBER,
        "medical_staff": UserRole.MEDICAL_STAFF,
        "patient": UserRole.PATIENT,
    }
    
    user_role = role_mapping.get(role, UserRole.PATIENT)
    
    user_profile = manager.create_user(
        user_id, username, user_role, email, phone,
        age, gender, health_status, family_id, medical_id
    )
    
    return user_profile.to_dict()

def create_family_api(
    family_id: str,
    family_name: str,
    admin_user_id: str,
) -> Dict:
    """创建家庭API"""
    manager = UserManager()
    
    result = manager.family_manager.create_family(
        family_id, family_name, admin_user_id
    )
    
    return result

def check_permission_api(
    user_id: str,
    permission: str,
) -> Dict:
    """检查权限API"""
    manager = UserManager()
    
    permission_mapping = {
        "view_own_data": Permission.VIEW_OWN_DATA,
        "edit_own_data": Permission.EDIT_OWN_DATA,
        "view_family_data": Permission.VIEW_FAMILY_DATA,
        "edit_family_data": Permission.EDIT_FAMILY_DATA,
        "manage_family_members": Permission.MANAGE_FAMILY_MEMBERS,
        "view_family_warnings": Permission.VIEW_FAMILY_WARNINGS,
        "receive_family_notifications": Permission.RECEIVE_FAMILY_NOTIFICATIONS,
    }
    
    perm = permission_mapping.get(permission, Permission.VIEW_OWN_DATA)
    
    has_perm = manager.check_permission(user_id, perm)
    
    return {
        "user_id": user_id,
        "permission": permission,
        "has_permission": has_perm,
    }

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("用户管理模块测试")
    print("=" * 60)
    
    # 测试创建家庭管理员
    user_result = create_user_api(
        user_id="zhang_aunt_001",
        username="张阿姨",
        role="family_admin",
        age=65,
        gender="女",
        health_status="糖尿病+高血压",
        family_id="family_001"
    )
    print(f"用户创建结果：{user_result}")
    
    # 测试创建家庭
    family_result = create_family_api(
        family_id="family_001",
        family_name="张家",
        admin_user_id="zhang_aunt_001"
    )
    print(f"家庭创建结果：{family_result}")
    
    # 测试权限检查
    perm_result = check_permission_api(
        user_id="zhang_aunt_001",
        permission="view_family_data"
    )
    print(f"权限检查结果：{perm_result}")
    
    print("=" * 60)