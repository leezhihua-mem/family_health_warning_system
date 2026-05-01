"""
医疗对接模块
医生端 + 医院端对接

创建时间：2026-05-01 22:08
版本：v1.0
开发者：天工Agent + 匠心Agent
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

# ============================================
# 医疗机构类型 ⭐⭐⭐⭐⭐
# ============================================

class MedicalInstitutionType(Enum):
    """医疗机构类型"""
    HOSPITAL = "hospital"  # 医院 ⭐⭐⭐⭐⭐
    CLINIC = "clinic"  # 诊所
    HEALTH_CENTER = "health_center"  # 健康中心 ⭐⭐⭐⭐⭐
    COMMUNITY_HEALTH = "community_health"  # 社区卫生站

# ============================================
# 医疗人员类型 ⭐⭐⭐⭐⭐
# ============================================

class MedicalStaffType(Enum):
    """医疗人员类型"""
    DOCTOR = "doctor"  # 医生 ⭐⭐⭐⭐⭐
    NURSE = "nurse"  # 护士
    HEALTH_MANAGER = "health_manager"  # 健康管理师 ⭐⭐⭐⭐⭐
    MEDICAL_ASSISTANT = "medical_assistant"  # 医疗助理

# ============================================
# 医疗机构档案 ⭐⭐⭐⭐⭐
# ============================================

class MedicalInstitution:
    """医疗机构档案"""
    
    def __init__(
        self,
        institution_id: str,
        institution_name: str,
        institution_type: MedicalInstitutionType,
        address: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
        license_number: Optional[str] = None,
    ):
        self.institution_id = institution_id
        self.institution_name = institution_name
        self.institution_type = institution_type
        self.address = address
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.license_number = license_number
        self.staff_members = []  # 医疗人员列表 ⭐⭐⭐⭐⭐
        self.patients = []  # 患者列表
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.is_active = True
    
    def add_staff_member(self, staff_id: str) -> bool:
        """添加医疗人员"""
        if staff_id not in self.staff_members:
            self.staff_members.append(staff_id)
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False
    
    def remove_staff_member(self, staff_id: str) -> bool:
        """移除医疗人员"""
        if staff_id in self.staff_members:
            self.staff_members.remove(staff_id)
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False
    
    def add_patient(self, patient_id: str) -> bool:
        """添加患者"""
        if patient_id not in self.patients:
            self.patients.append(patient_id)
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False
    
    def remove_patient(self, patient_id: str) -> bool:
        """移除患者"""
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "institution_id": self.institution_id,
            "institution_name": self.institution_name,
            "institution_type": self.institution_type.value,
            "address": self.address,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "license_number": self.license_number,
            "staff_members": self.staff_members,
            "patients": self.patients,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }

# ============================================
# 医疗人员档案 ⭐⭐⭐⭐⭐
# ============================================

class MedicalStaffProfile:
    """医疗人员档案"""
    
    def __init__(
        self,
        staff_id: str,
        staff_name: str,
        staff_type: MedicalStaffType,
        institution_id: str,
        specialization: Optional[str] = None,
        license_number: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
    ):
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.staff_type = staff_type
        self.institution_id = institution_id  # 所属医疗机构 ⭐⭐⭐⭐⭐
        self.specialization = specialization  # 专业领域 ⭐⭐⭐⭐⭐
        self.license_number = license_number
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.assigned_patients = []  # 负责的患者 ⭐⭐⭐⭐⭐
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.is_active = True
    
    def assign_patient(self, patient_id: str) -> bool:
        """分配患者"""
        if patient_id not in self.assigned_patients:
            self.assigned_patients.append(patient_id)
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False
    
    def unassign_patient(self, patient_id: str) -> bool:
        """取消分配患者"""
        if patient_id in self.assigned_patients:
            self.assigned_patients.remove(patient_id)
            self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "staff_id": self.staff_id,
            "staff_name": self.staff_name,
            "staff_type": self.staff_type.value,
            "institution_id": self.institution_id,
            "specialization": self.specialization,
            "license_number": self.license_number,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "assigned_patients": self.assigned_patients,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }

# ============================================
# 医疗对接管理器 ⭐⭐⭐⭐⭐
# ============================================

class MedicalIntegrationManager:
    """医疗对接管理器"""
    
    def __init__(self):
        self.institutions = {}  # 医疗机构ID -> 医疗机构档案
        self.staff = {}  # 医疗人员ID -> 医疗人员档案
        self.patient_institution_mapping = {}  # 患者ID -> 医疗机构列表
        self.patient_staff_mapping = {}  # 患者ID -> 医疗人员列表
    
    def create_institution(
        self,
        institution_id: str,
        institution_name: str,
        institution_type: str,
        address: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
        license_number: Optional[str] = None,
    ) -> MedicalInstitution:
        """
        创建医疗机构
        
        Args:
            institution_id: 医疗机构ID
            institution_name: 医疗机构名称
            institution_type: 医疗机构类型
            address: 地址
            contact_phone: 联系电话
            contact_email: 联系邮箱
            license_number: 执业许可证号
        
        Returns:
            MedicalInstitution: 医疗机构档案
        """
        # 转换医疗机构类型
        type_mapping = {
            "hospital": MedicalInstitutionType.HOSPITAL,
            "clinic": MedicalInstitutionType.CLINIC,
            "health_center": MedicalInstitutionType.HEALTH_CENTER,
            "community_health": MedicalInstitutionType.COMMUNITY_HEALTH,
        }
        
        inst_type = type_mapping.get(institution_type, MedicalInstitutionType.HOSPITAL)
        
        institution = MedicalInstitution(
            institution_id=institution_id,
            institution_name=institution_name,
            institution_type=inst_type,
            address=address,
            contact_phone=contact_phone,
            contact_email=contact_email,
            license_number=license_number,
        )
        
        self.institutions[institution_id] = institution
        
        return institution
    
    def create_staff(
        self,
        staff_id: str,
        staff_name: str,
        staff_type: str,
        institution_id: str,
        specialization: Optional[str] = None,
        license_number: Optional[str] = None,
        contact_phone: Optional[str] = None,
        contact_email: Optional[str] = None,
    ) -> MedicalStaffProfile:
        """
        创建医疗人员
        
        Args:
            staff_id: 医疗人员ID
            staff_name: 医疗人员姓名
            staff_type: 医疗人员类型
            institution_id: 所属医疗机构ID
            specialization: 专业领域
            license_number: 执业许可证号
            contact_phone: 联系电话
            contact_email: 联系邮箱
        
        Returns:
            MedicalStaffProfile: 医疗人员档案
        """
        # 转换医疗人员类型
        type_mapping = {
            "doctor": MedicalStaffType.DOCTOR,
            "nurse": MedicalStaffType.NURSE,
            "health_manager": MedicalStaffType.HEALTH_MANAGER,
            "medical_assistant": MedicalStaffType.MEDICAL_ASSISTANT,
        }
        
        staf_type = type_mapping.get(staff_type, MedicalStaffType.DOCTOR)
        
        staff_profile = MedicalStaffProfile(
            staff_id=staff_id,
            staff_name=staff_name,
            staff_type=staf_type,
            institution_id=institution_id,
            specialization=specialization,
            license_number=license_number,
            contact_phone=contact_phone,
            contact_email=contact_email,
        )
        
        self.staff[staff_id] = staff_profile
        
        # 添加到医疗机构
        if institution_id in self.institutions:
            self.institutions[institution_id].add_staff_member(staff_id)
        
        return staff_profile
    
    def assign_patient_to_staff(
        self,
        patient_id: str,
        staff_id: str,
    ) -> bool:
        """
        分配患者到医疗人员
        
        Args:
            patient_id: 患者ID
            staff_id: 医疗人员ID
        
        Returns:
            bool: 分配是否成功
        """
        if staff_id not in self.staff:
            return False
        
        # 添加到医疗人员的负责患者列表
        self.staff[staff_id].assign_patient(patient_id)
        
        # 更新患者映射
        if patient_id not in self.patient_staff_mapping:
            self.patient_staff_mapping[patient_id] = []
        
        if staff_id not in self.patient_staff_mapping[patient_id]:
            self.patient_staff_mapping[patient_id].append(staff_id)
        
        return True
    
    def assign_patient_to_institution(
        self,
        patient_id: str,
        institution_id: str,
    ) -> bool:
        """
        分配患者到医疗机构
        
        Args:
            patient_id: 患者ID
            institution_id: 医疗机构ID
        
        Returns:
            bool: 分配是否成功
        """
        if institution_id not in self.institutions:
            return False
        
        # 添加到医疗机构的患者列表
        self.institutions[institution_id].add_patient(patient_id)
        
        # 更新患者映射
        if patient_id not in self.patient_institution_mapping:
            self.patient_institution_mapping[patient_id] = []
        
        if institution_id not in self.patient_institution_mapping[patient_id]:
            self.patient_institution_mapping[patient_id].append(institution_id)
        
        return True
    
    def get_patient_staff(self, patient_id: str) -> List[MedicalStaffProfile]:
        """
        获取患者的医疗人员列表
        
        Args:
            patient_id: 患者ID
        
        Returns:
            List[MedicalStaffProfile]: 医疗人员列表
        """
        staff_ids = self.patient_staff_mapping.get(patient_id, [])
        
        return [
            self.staff.get(staff_id)
            for staff_id in staff_ids
            if self.staff.get(staff_id)
        ]
    
    def get_patient_institutions(self, patient_id: str) -> List[MedicalInstitution]:
        """
        获取患者的医疗机构列表
        
        Args:
            patient_id: 患者ID
        
        Returns:
            List[MedicalInstitution]: 医疗机构列表
        """
        institution_ids = self.patient_institution_mapping.get(patient_id, [])
        
        return [
            self.institutions.get(inst_id)
            for inst_id in institution_ids
            if self.institutions.get(inst_id)
        ]
    
    def get_staff_patients(self, staff_id: str) -> List[str]:
        """
        获取医疗人员负责的患者列表
        
        Args:
            staff_id: 医疗人员ID
        
        Returns:
            List[str]: 患者ID列表
        """
        if staff_id in self.staff:
            return self.staff[staff_id].assigned_patients
        
        return []
    
    def get_institution_patients(self, institution_id: str) -> List[str]:
        """
        获取医疗机构的患者列表
        
        Args:
            institution_id: 医疗机构ID
        
        Returns:
            List[str]: 患者ID列表
        """
        if institution_id in self.institutions:
            return self.institutions[institution_id].patients
        
        return []

# ============================================
# 医疗预警通知 ⭐⭐⭐⭐⭐
# ============================================

class MedicalNotificationManager:
    """医疗预警通知管理器"""
    
    def __init__(self):
        self.notifications = {}  # 通知ID -> 通知内容
    
    def send_warning_notification(
        self,
        patient_id: str,
        warning_data: Dict,
        staff_ids: List[str],
    ) -> Dict:
        """
        发送预警通知给医疗人员
        
        Args:
            patient_id: 患者ID
            warning_data: 预警数据
            staff_ids: 医疗人员ID列表
        
        Returns:
            Dict: 通知结果
        """
        notification_id = f"medical_notify_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        notification = {
            "notification_id": notification_id,
            "patient_id": patient_id,
            "warning_level": warning_data.get("warning_level", ""),
            "warning_type": warning_data.get("warning_type", ""),
            "explanation": warning_data.get("explanation", ""),
            "suggestion": warning_data.get("suggestion", []),
            "staff_ids": staff_ids,
            "sent_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "sent",
        }
        
        self.notifications[notification_id] = notification
        
        return notification
    
    def get_patient_notifications(
        self,
        patient_id: str,
        limit: int = 100,
    ) -> List[Dict]:
        """
        获取患者的医疗通知
        
        Args:
            patient_id: 患者ID
            limit: 限制数量
        
        Returns:
            List[Dict]: 通知列表
        """
        patient_notifications = [
            n for n in self.notifications.values()
            if n["patient_id"] == patient_id
        ]
        
        # 按时间排序
        patient_notifications.sort(
            key=lambda x: x["sent_at"],
            reverse=True
        )
        
        return patient_notifications[:limit]

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

def create_institution_api(
    institution_id: str,
    institution_name: str,
    institution_type: str,
    address: Optional[str] = None,
    contact_phone: Optional[str] = None,
    contact_email: Optional[str] = None,
    license_number: Optional[str] = None,
) -> Dict:
    """创建医疗机构API"""
    manager = MedicalIntegrationManager()
    
    institution = manager.create_institution(
        institution_id, institution_name, institution_type,
        address, contact_phone, contact_email, license_number
    )
    
    return institution.to_dict()

def create_staff_api(
    staff_id: str,
    staff_name: str,
    staff_type: str,
    institution_id: str,
    specialization: Optional[str] = None,
    license_number: Optional[str] = None,
    contact_phone: Optional[str] = None,
    contact_email: Optional[str] = None,
) -> Dict:
    """创建医疗人员API"""
    manager = MedicalIntegrationManager()
    
    staff_profile = manager.create_staff(
        staff_id, staff_name, staff_type, institution_id,
        specialization, license_number, contact_phone, contact_email
    )
    
    return staff_profile.to_dict()

def assign_patient_to_staff_api(
    patient_id: str,
    staff_id: str,
) -> Dict:
    """分配患者到医疗人员API"""
    manager = MedicalIntegrationManager()
    
    result = manager.assign_patient_to_staff(patient_id, staff_id)
    
    return {
        "patient_id": patient_id,
        "staff_id": staff_id,
        "assigned": result,
    }

def send_medical_notification_api(
    patient_id: str,
    warning_data: Dict,
    staff_ids: List[str],
) -> Dict:
    """发送医疗预警通知API"""
    manager = MedicalNotificationManager()
    
    notification = manager.send_warning_notification(
        patient_id, warning_data, staff_ids
    )
    
    return notification

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("医疗对接模块测试")
    print("=" * 60)
    
    # 测试创建医疗机构
    institution_result = create_institution_api(
        institution_id="hospital_001",
        institution_name="北京协和医院",
        institution_type="hospital",
        address="北京市东城区",
        contact_phone="010-12345678"
    )
    print(f"医疗机构创建结果：{institution_result}")
    
    # 测试创建医疗人员
    staff_result = create_staff_api(
        staff_id="doctor_001",
        staff_name="李医生",
        staff_type="doctor",
        institution_id="hospital_001",
        specialization="内分泌科"
    )
    print(f"医疗人员创建结果：{staff_result}")
    
    # 测试分配患者
    assign_result = assign_patient_to_staff_api(
        patient_id="zhang_aunt_001",
        staff_id="doctor_001"
    )
    print(f"患者分配结果：{assign_result}")
    
    # 测试医疗通知
    notify_result = send_medical_notification_api(
        patient_id="zhang_aunt_001",
        warning_data={
            "warning_level": "S",
            "warning_type": "DKA",
            "explanation": "酮症酸中毒预警",
            "suggestion": ["立即就医"]
        },
        staff_ids=["doctor_001"]
    )
    print(f"医疗通知结果：{notify_result}")
    
    print("=" * 60)