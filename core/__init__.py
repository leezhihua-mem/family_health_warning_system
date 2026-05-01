"""
核心模块包
"""

from .engine import (
    WarningState,
    warning_executor_node,
    mirror_validator_node,
    build_warning_graph,
    generate_warning
)

from .validator import MirrorValidator

from .notification import (
    NotificationChannel,
    NotificationStrategy,
    NotificationMessage,
    NotificationManager,
    NotificationTemplate,
    send_notification_api,
    get_notification_history_api
)

from .analytics import (
    HealthTrendAnalyzer,
    WarningStatisticsAnalyzer,
    DataVisualizationGenerator,
    analyze_health_trend_api,
    analyze_warning_stats_api
)

from .user_management import (
    UserRole,
    Permission,
    UserProfile,
    FamilyManager,
    UserManager,
    create_user_api,
    create_family_api,
    check_permission_api,
)

from .medical_integration import (
    MedicalInstitutionType,
    MedicalStaffType,
    MedicalInstitution,
    MedicalStaffProfile,
    MedicalIntegrationManager,
    MedicalNotificationManager,
    create_institution_api,
    create_staff_api,
    assign_patient_to_staff_api,
    send_medical_notification_api,
)

__all__ = [
    # Core Engine
    "WarningState",
    "warning_executor_node",
    "mirror_validator_node",
    "build_warning_graph",
    "generate_warning",
    "MirrorValidator",
    # Notification
    "NotificationChannel",
    "NotificationStrategy",
    "NotificationMessage",
    "NotificationManager",
    "NotificationTemplate",
    "send_notification_api",
    "get_notification_history_api",
    # Analytics
    "HealthTrendAnalyzer",
    "WarningStatisticsAnalyzer",
    "DataVisualizationGenerator",
    "analyze_health_trend_api",
    "analyze_warning_stats_api",
    # User Management
    "UserRole",
    "Permission",
    "UserProfile",
    "FamilyManager",
    "UserManager",
    "create_user_api",
    "create_family_api",
    "check_permission_api",
    # Medical Integration
    "MedicalInstitutionType",
    "MedicalStaffType",
    "MedicalInstitution",
    "MedicalStaffProfile",
    "MedicalIntegrationManager",
    "MedicalNotificationManager",
    "create_institution_api",
    "create_staff_api",
    "assign_patient_to_staff_api",
    "send_medical_notification_api",
]