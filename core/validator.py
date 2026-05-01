"""
明镜验证模块
强制验证闭环核心

创建时间：2026-05-01 16:25
版本：v1.0
开发者：明镜Agent
"""

from typing import Dict, List, Optional

class MirrorValidator:
    """
    明镜验证器
    核心职责：try to break it（攻击性验证）
    """
    
    def __init__(self):
        self.name = "明镜"
        self.role = "验证Agent"
    
    def validate(self, warning_result: Optional[dict], input_data: dict) -> dict:
        """
        执行完整验证流程
        """
        errors = []
        score = 100.0
        
        if warning_result is None:
            # 无预警=正常，直接通过
            return {
                "status": "pass",
                "errors": [],
                "score": 100.0
            }
        
        # 1. 数据准确性验证 ⭐⭐⭐⭐⭐
        if not self._validate_data_accuracy(warning_result, input_data):
            errors.append("数据准确性验证失败")
            score -= 30
        
        # 2. 逻辑一致性验证
        if not self._validate_logic_consistency(warning_result):
            errors.append("逻辑一致性验证失败")
            score -= 20
        
        # 3. 边界情况验证 ⭐⭐⭐⭐⭐
        if not self._validate_edge_cases(warning_result, input_data):
            errors.append("边界情况验证失败")
            score -= 20
        
        # 4. try to break it（攻击性测试）⭐⭐⭐⭐⭐
        if not self._try_to_break_it(warning_result, input_data):
            errors.append("攻击性测试失败")
            score -= 30
        
        # 返回验证结果
        if len(errors) == 0:
            status = "pass"
        else:
            status = "fail"
        
        return {
            "status": status,
            "errors": errors,
            "score": score
        }
    
    def _validate_data_accuracy(self, result: dict, input_data: dict) -> bool:
        """数据准确性验证"""
        # 检查数据来源是否验证
        if not input_data.get("data_verified"):
            return False
        
        # 检查数据时间是否合理
        if not input_data.get("data_time"):
            return False
        
        return True
    
    def _validate_logic_consistency(self, result: dict) -> bool:
        """逻辑一致性验证"""
        # 检查预警等级
        level = result.get("warning_level")
        if level not in ["S", "A", "B", "C"]:
            return False
        
        # 检查可解释性 ⭐⭐⭐⭐⭐
        if not result.get("explanation"):
            return False
        
        # 检查循证医学依据
        if not result.get("evidence"):
            return False
        
        return True
    
    def _validate_edge_cases(self, result: dict, input_data: dict) -> bool:
        """边界情况验证 ⭐⭐⭐⭐⭐"""
        # 检查极端值
        warning_id = result.get("warning_id", "")
        
        if "DKA" in warning_id:
            glucose = input_data.get("glucose_value", 0)
            ketone = input_data.get("ketone_value", 0)
            
            # DKA阈值：血糖>13.9 + 血酮≥3.0
            if glucose > 33.3 and result["warning_level"] != "S":
                return False
            
            if ketone > 5.0 and result["warning_level"] != "S":
                return False
        
        return True
    
    def _try_to_break_it(self, result: dict, input_data: dict) -> bool:
        """
        try to break it核心验证 ⭐⭐⭐⭐⭐
        主动找漏洞、找错误
        """
        level = result.get("warning_level")
        suggestion = result.get("suggestion", [])
        
        # 1. 检查阈值合理性
        warning_id = result.get("warning_id", "")
        
        if "DKA" in warning_id:
            glucose = input_data.get("glucose_value", 0)
            ketone = input_data.get("ketone_value", 0)
            
            # DKA阈值验证
            if glucose <= 13.9 or ketone < 3.0:
                if level == "S":
                    return False  # 阈值不符合DKA标准
        
        # 2. 检查建议合理性 ⭐⭐⭐⭐⭐
        if level in ["S", "A"]:
            # S级必须建议就医
            if "就医" not in str(suggestion):
                return False
        
        # 3. 检查循证医学依据完整性
        evidence = result.get("evidence", "")
        if not evidence or len(evidence) < 10:
            return False
        
        return True
    
    def get_name(self) -> str:
        """返回Agent名称"""
        return self.name
    
    def get_role(self) -> str:
        """返回Agent角色"""
        return self.role

# ============================================
# 测试验证
# ============================================

if __name__ == "__main__":
    validator = MirrorValidator()
    
    print("=" * 60)
    print("明镜验证器测试")
    print("=" * 60)
    
    # 测试DKA预警（S级）
    test_result = {
        "warning_id": "DKA_20260501_162000",
        "warning_level": "S",
        "explanation": "高血糖(15.0mmol/L) + 高血酮(3.5mmol/L)",
        "suggestion": ["立即就医", "补液治疗"],
        "evidence": "ADA糖尿病酮症酸中毒指南2025"
    }
    
    test_input = {
        "glucose_value": 15.0,
        "ketone_value": 3.5,
        "data_verified": True,
        "data_time": "2026-05-01 16:00:00"
    }
    
    validation_result = validator.validate(test_result, test_input)
    
    print(f"验证状态：{validation_result['status']}")
    print(f"验证评分：{validation_result['score']}")
    print(f"验证错误：{validation_result['errors']}")
    
    print("=" * 60)