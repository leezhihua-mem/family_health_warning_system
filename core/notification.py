"""
预警推送模块
多渠道推送：App + 短信 + 电话 + 120

创建时间：2026-05-01 19:42
版本：v1.0
开发者：流光Agent
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

# ============================================
# 推送渠道定义 ⭐⭐⭐⭐⭐
# ============================================

class NotificationChannel(Enum):
    """推送渠道"""
    APP = "App"
    SMS = "短信"
    PHONE = "电话"
    EMERGENCY_120 = "120急救"
    EMAIL = "邮件"
    WECHAT = "微信"

# ============================================
# 预警分级推送策略 ⭐⭐⭐⭐⭐
# ============================================

class NotificationStrategy:
    """推送策略"""
    
    # S级（红色紧急）推送策略 ⭐⭐⭐⭐⭐
    S_LEVEL_CHANNELS = [
        NotificationChannel.APP,
        NotificationChannel.SMS,
        NotificationChannel.PHONE,
        NotificationChannel.EMERGENCY_120
    ]
    
    # A级（黄色高风险）推送策略
    A_LEVEL_CHANNELS = [
        NotificationChannel.APP,
        NotificationChannel.SMS
    ]
    
    # B级（绿色中等）推送策略
    B_LEVEL_CHANNELS = [
        NotificationChannel.APP
    ]
    
    # C级（白色低风险）推送策略
    C_LEVEL_CHANNELS = []
    
    @staticmethod
    def get_channels(warning_level: str) -> List[NotificationChannel]:
        """根据预警等级获取推送渠道"""
        if warning_level == "S":
            return NotificationStrategy.S_LEVEL_CHANNELS
        elif warning_level == "A":
            return NotificationStrategy.A_LEVEL_CHANNELS
        elif warning_level == "B":
            return NotificationStrategy.B_LEVEL_CHANNELS
        else:
            return NotificationStrategy.C_LEVEL_CHANNELS

# ============================================
# 推送消息结构 ⭐⭐⭐⭐⭐
# ============================================

class NotificationMessage:
    """推送消息结构"""
    
    def __init__(
        self,
        user_id: str,
        warning_level: str,
        warning_type: str,
        explanation: str,
        suggestion: List[str],
        channels: List[NotificationChannel]
    ):
        self.user_id = user_id
        self.warning_level = warning_level
        self.warning_type = warning_type
        self.explanation = explanation
        self.suggestion = suggestion
        self.channels = channels
        self.send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = "pending"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "warning_level": self.warning_level,
            "warning_type": self.warning_type,
            "explanation": self.explanation,
            "suggestion": self.suggestion,
            "channels": [ch.value for ch in self.channels],
            "send_time": self.send_time,
            "status": self.status
        }

# ============================================
# 推送管理器 ⭐⭐⭐⭐⭐
# ============================================

class NotificationManager:
    """推送管理器"""
    
    def __init__(self):
        self.name = "预警推送管理器"
        self.notification_history = []
    
    def send_notification(
        self,
        user_id: str,
        warning_output: Dict,
        warning_level: str
    ) -> Dict:
        """
        发送预警推送
        
        Args:
            user_id: 用户ID
            warning_output: 预警输出
            warning_level: 预警等级
        
        Returns:
            Dict: 推送结果
        """
        # 获取推送渠道
        channels = NotificationStrategy.get_channels(warning_level)
        
        # 创建推送消息
        message = NotificationMessage(
            user_id=user_id,
            warning_level=warning_level,
            warning_type=warning_output.get("warning_type", ""),
            explanation=warning_output.get("explanation", ""),
            suggestion=warning_output.get("suggestion", []),
            channels=channels
        )
        
        # 执行推送
        push_results = []
        for channel in channels:
            result = self._push_to_channel(channel, message)
            push_results.append(result)
        
        # 更新状态
        message.status = "sent"
        
        # 记录推送历史
        self.notification_history.append(message.to_dict())
        
        return {
            "success": True,
            "message": message.to_dict(),
            "push_results": push_results
        }
    
    def _push_to_channel(
        self,
        channel: NotificationChannel,
        message: NotificationMessage
    ) -> Dict:
        """
        推送到指定渠道
        
        Args:
            channel: 推送渠道
            message: 推送消息
        
        Returns:
            Dict: 推送结果
        """
        # 模拟推送逻辑（实际需要对接各渠道API）
        result = {
            "channel": channel.value,
            "status": "success",
            "send_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "message_id": f"{channel.value}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        # S级特殊处理 ⭐⭐⭐⭐⭐
        if message.warning_level == "S" and channel == NotificationChannel.EMERGENCY_120:
            result["emergency"] = True
            result["note"] = "自动拨打120急救电话（模拟）"
        
        return result
    
    def get_notification_history(self, user_id: str) -> List[Dict]:
        """
        获取用户推送历史
        
        Args:
            user_id: 用户ID
        
        Returns:
            List[Dict]: 推送历史
        """
        return [
            h for h in self.notification_history
            if h["user_id"] == user_id
        ]
    
    def clear_history(self) -> None:
        """清空推送历史"""
        self.notification_history = []

# ============================================
# 推送模板 ⭐⭐⭐⭐⭐
# ============================================

class NotificationTemplate:
    """推送模板"""
    
    @staticmethod
    def generate_app_message(warning_level: str, explanation: str, suggestion: List[str]) -> str:
        """生成App推送消息"""
        level_text = {
            "S": "🔴 紧急预警",
            "A": "🟡 高风险预警",
            "B": "🟢 中等风险预警",
            "C": "⚪ 低风险提示"
        }
        
        template = f"""
{level_text.get(warning_level, '预警')} ⭐⭐⭐⭐⭐

{explanation}

建议措施：
{suggestion}

时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return template
    
    @staticmethod
    def generate_sms_message(warning_level: str, explanation: str) -> str:
        """生成短信推送消息"""
        level_text = {
            "S": "紧急预警",
            "A": "高风险预警",
            "B": "中等风险预警",
            "C": "低风险提示"
        }
        
        template = f"""
【家庭健康预警】{level_text.get(warning_level, '预警')}

{explanation}

请及时处理！时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        return template
    
    @staticmethod
    def generate_emergency_message(warning_level: str, explanation: str) -> str:
        """生成紧急预警消息（120）⭐⭐⭐⭐⭐"""
        template = f"""
紧急医疗预警 ⭐⭐⭐⭐⭐

预警等级：{warning_level}
预警说明：{explanation}

自动拨打120急救电话...
时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return template

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

def send_notification_api(
    user_id: str,
    warning_output: Dict,
    warning_level: str
) -> Dict:
    """
    发送预警推送API
    
    Args:
        user_id: 用户ID
        warning_output: 预警输出
        warning_level: 预警等级
    
    Returns:
        Dict: 推送结果
    """
    manager = NotificationManager()
    
    result = manager.send_notification(user_id, warning_output, warning_level)
    
    return result

def get_notification_history_api(user_id: str) -> List[Dict]:
    """
    获取推送历史API
    
    Args:
        user_id: 用户ID
    
    Returns:
        List[Dict]: 推送历史
    """
    manager = NotificationManager()
    
    return manager.get_notification_history(user_id)

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("预警推送模块测试")
    print("=" * 60)
    
    # 测试S级预警推送
    warning_output = {
        "warning_type": "酮症酸中毒联合预警",
        "explanation": "高血糖(15.0mmol/L) + 高血酮(3.5mmol/L)",
        "suggestion": ["立即就医", "补液治疗", "胰岛素治疗"]
    }
    
    result = send_notification_api(
        user_id="zhang_aunt_001",
        warning_output=warning_output,
        warning_level="S"
    )
    
    print(f"推送结果：{result}")
    
    # 测试推送历史
    history = get_notification_history_api("zhang_aunt_001")
    print(f"推送历史：{history}")
    
    print("=" * 60)