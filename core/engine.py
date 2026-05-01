"""
家庭健康预警系统核心引擎
Phase 1开发 - 预警引擎核心代码

创建时间：2026-05-01 16:20
版本：v1.0
开发者：磐石Agent + 天工Agent + 明镜Agent
"""

# 导入核心模块
from datetime import datetime
from typing import TypedDict, Optional, List, Dict, Annotated
import operator

# 导入LangGraph
from langgraph.graph import StateGraph, END

# 导入25个预警模型
from models.warning_models import (
    # 11个单项预警
    blood_pressure_warning_algorithm,
    pulse_pressure_warning_algorithm,
    morning_hypertension_warning_algorithm,
    ecg_warning_algorithm,
    spo2_warning_algorithm,
    hrv_warning_algorithm,
    glucose_warning_algorithm,
    ketone_warning_algorithm,
    uric_acid_warning_algorithm,
    temperature_warning_algorithm,
    weight_warning_algorithm,
    # 12个联合预警
    dka_warning_algorithm,
    stroke_warning_algorithm,
    ami_warning_algorithm,
    osa_warning_algorithm,
    metabolic_syndrome_warning_algorithm,
    respiratory_failure_warning_algorithm,
    heart_failure_warning_algorithm,
    hypoglycemia_coma_warning_algorithm,
    hhs_warning_algorithm,
    sepsis_warning_algorithm,
    arrhythmia_death_warning_algorithm,
    gout_warning_algorithm,
    # 2个专项预警
    stroke_complete_warning_algorithm,
    ami_complete_warning_algorithm
)

# 导入验证模块
from core.validator import MirrorValidator

# ============================================
# State定义（LangGraph核心）⭐⭐⭐⭐⭐
# ============================================

class WarningState(TypedDict):
    """预警系统State定义"""
    # 任务信息
    user_id: str
    warning_model_id: str  # 01-25
    input_data: dict
    
    # 预警结果
    warning_output: Optional[dict]
    warning_level: str  # S/A/B/C
    
    # 验证状态
    validation_status: str  # pending/pass/fail
    validation_errors: Annotated[List[str], operator.add]
    validation_score: float
    
    # 重试机制
    retry_count: int
    max_retry: int
    
    # 时间戳
    start_time: str
    end_time: Optional[str]

# ============================================
# 预警执行节点 ⭐⭐⭐⭐⭐
# ============================================

def warning_executor_node(state: WarningState) -> WarningState:
    """
    预警执行节点
    根据模型ID调用对应预警算法
    """
    model_id = state["warning_model_id"]
    input_data = state["input_data"]
    
    # 模型映射
    model_functions = {
        "01": blood_pressure_warning_algorithm,
        "02": pulse_pressure_warning_algorithm,
        "03": morning_hypertension_warning_algorithm,
        "04": ecg_warning_algorithm,
        "05": spo2_warning_algorithm,
        "06": hrv_warning_algorithm,
        "07": glucose_warning_algorithm,
        "08": ketone_warning_algorithm,
        "09": uric_acid_warning_algorithm,
        "10": temperature_warning_algorithm,
        "11": weight_warning_algorithm,
        "12": dka_warning_algorithm,  # DKA ⭐⭐⭐⭐⭐
        "13": stroke_warning_algorithm,
        "14": ami_warning_algorithm,
        "15": osa_warning_algorithm,
        "16": metabolic_syndrome_warning_algorithm,
        "17": respiratory_failure_warning_algorithm,
        "18": heart_failure_warning_algorithm,
        "19": hypoglycemia_coma_warning_algorithm,
        "20": hhs_warning_algorithm,
        "21": sepsis_warning_algorithm,
        "22": arrhythmia_death_warning_algorithm,
        "23": gout_warning_algorithm,
        "24": stroke_complete_warning_algorithm,  # 脑卒中专项 ⭐⭐⭐⭐⭐
        "25": ami_complete_warning_algorithm  # 心梗专项 ⭐⭐⭐⭐⭐
    }
    
    # 执行预警
    model_func = model_functions.get(model_id)
    if model_func:
        result = model_func(input_data)
    else:
        result = None
    
    # 更新State
    state["warning_output"] = result
    if result:
        state["warning_level"] = result.get("warning_level", "C")
    else:
        state["warning_level"] = "C"
    
    state["start_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return state

# ============================================
# 明镜验证节点 ⭐⭐⭐⭐⭐
# ============================================

def mirror_validator_node(state: WarningState) -> WarningState:
    """
    明镜验证节点
    强制验证：try to break it
    """
    validator = MirrorValidator()
    
    result = state["warning_output"]
    input_data = state["input_data"]
    
    # 执行验证
    validation_result = validator.validate(result, input_data)
    
    # 更新State
    state["validation_status"] = validation_result["status"]
    state["validation_errors"] = validation_result["errors"]
    state["validation_score"] = validation_result["score"]
    
    if state["validation_status"] == "fail":
        state["retry_count"] += 1
    
    state["end_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return state

# ============================================
# LangGraph编排 ⭐⭐⭐⭐⭐
# ============================================

def build_warning_graph() -> StateGraph:
    """
    构建预警系统LangGraph
    强制验证闭环
    """
    graph = StateGraph(WarningState)
    
    # 添加节点
    graph.add_node("executor", warning_executor_node)
    graph.add_node("validator", mirror_validator_node)  # 强制验证 ⭐⭐⭐⭐⭐
    
    # 设置入口
    graph.set_entry_point("executor")
    
    # 强制验证闭环 ⭐⭐⭐⭐⭐
    graph.add_edge("executor", "validator")
    
    # 验证路由
    def route_validation(state):
        if state["validation_status"] == "pass":
            return END
        elif state["retry_count"] < state["max_retry"]:
            return "executor"  # 回退重试 ⭐⭐⭐⭐⭐
        else:
            return END
    
    graph.add_conditional_edges("validator", route_validation)
    
    return graph

# ============================================
# API入口 ⭐⭐⭐⭐⭐
# ============================================

def generate_warning(user_id: str, model_id: str, input_data: dict) -> dict:
    """
    预警生成API
    """
    # 构建Graph
    graph = build_warning_graph()
    app = graph.compile()
    
    # 初始化State
    initial_state = WarningState(
        user_id=user_id,
        warning_model_id=model_id,
        input_data=input_data,
        warning_output=None,
        warning_level="C",
        validation_status="pending",
        validation_errors=[],
        validation_score=100.0,
        retry_count=0,
        max_retry=3,
        start_time="",
        end_time=None
    )
    
    # 执行Graph ⭐⭐⭐⭐⭐
    final_state = app.invoke(initial_state)
    
    return {
        "warning_output": final_state["warning_output"],
        "warning_level": final_state["warning_level"],
        "validation_status": final_state["validation_status"],
        "validation_score": final_state["validation_score"]
    }

# ============================================
# 测试入口
# ============================================

if __name__ == "__main__":
    # 测试DKA预警（张阿姨场景）⭐⭐⭐⭐⭐
    result = generate_warning(
        user_id="zhang_aunt",
        model_id="12",
        input_data={
            "glucose_value": 15.0,
            "ketone_value": 3.5,
            "data_verified": True
        }
    )
    
    print("=" * 60)
    print("家庭健康预警系统测试")
    print("=" * 60)
    print(f"预警等级：{result['warning_level']}")
    print(f"验证状态：{result['validation_status']}")
    print(f"验证评分：{result['validation_score']}")
    print("=" * 60)