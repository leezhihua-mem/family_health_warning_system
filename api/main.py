"""
家庭健康预警系统 API服务
FastAPI实现

创建时间：2026-05-01 16:58
版本：v1.0
开发者：磐石Agent + 流光Agent
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
sys.path.append('/Users/lizhihua/.openclaw/workspace/family_health_warning_system')

from core.engine import generate_warning

# ============================================
# FastAPI应用初始化 ⭐⭐⭐⭐⭐
# ============================================

app = FastAPI(
    title="家庭健康预警服务系统",
    description="基于25个预警模型的多维度健康预警平台",
    version="v1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================
# 数据模型定义（Pydantic）⭐⭐⭐⭐⭐
# ============================================

class WarningRequest(BaseModel):
    """预警请求数据模型"""
    user_id: str
    model_id: str  # 01-25
    input_data: Dict[str, Any]
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "zhang_aunt_001",
                "model_id": "12",
                "input_data": {
                    "glucose_value": 15.0,
                    "ketone_value": 3.5,
                    "data_verified": True,
                    "data_time": "2026-05-01 16:00:00"
                }
            }
        }

class WarningResponse(BaseModel):
    """预警响应数据模型"""
    warning_output: Optional[Dict]
    warning_level: str
    validation_status: str
    validation_score: float
    retry_count: int
    
    class Config:
        schema_extra = {
            "example": {
                "warning_output": {
                    "warning_id": "DKA_20260501_160000",
                    "explanation": "高血糖(15.0mmol/L) + 高血酮(3.5mmol/L)",
                    "suggestion": ["立即就医", "补液治疗"],
                    "evidence": "ADA糖尿病酮症酸中毒指南2025"
                },
                "warning_level": "S",
                "validation_status": "pass",
                "validation_score": 100.0,
                "retry_count": 0
            }
        }

class HealthCheckResponse(BaseModel):
    """健康检查响应"""
    status: str
    version: str
    models_count: int
    timestamp: str

# ============================================
# API路由定义 ⭐⭐⭐⭐⭐
# ============================================

@app.get("/", tags=["根路径"])
async def root():
    """API根路径"""
    return {
        "message": "家庭健康预警服务系统 API",
        "version": "v1.0",
        "docs": "/docs",
        "models": 25
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["健康检查"])
async def health_check():
    """
    API健康检查
    验证服务是否正常运行 ⭐⭐⭐⭐⭐
    """
    return HealthCheckResponse(
        status="healthy",
        version="v1.0",
        models_count=25,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.get("/models/list", tags=["模型管理"])
async def list_models():
    """
    列出所有预警模型
    返回25个预警模型清单 ⭐⭐⭐⭐⭐
    """
    models = [
        {"id": "01", "name": "血压预警", "type": "单项预警"},
        {"id": "02", "name": "脉压差预警", "type": "单项预警"},
        {"id": "03", "name": "晨峰高血压预警", "type": "单项预警"},
        {"id": "04", "name": "心电预警", "type": "单项预警"},
        {"id": "05", "name": "血氧预警", "type": "单项预警"},
        {"id": "06", "name": "HRV预警", "type": "单项预警"},
        {"id": "07", "name": "血糖预警", "type": "单项预警"},
        {"id": "08", "name": "血酮预警", "type": "单项预警"},
        {"id": "09", "name": "尿酸预警", "type": "单项预警"},
        {"id": "10", "name": "体温预警", "type": "单项预警"},
        {"id": "11", "name": "体重预警", "type": "单项预警"},
        {"id": "12", "name": "酮症酸中毒联合预警", "type": "联合预警 ⭐⭐⭐⭐⭐"},
        {"id": "13", "name": "脑卒中风险联合预警", "type": "联合预警"},
        {"id": "14", "name": "心梗风险联合预警", "type": "联合预警"},
        {"id": "15", "name": "睡眠呼吸暂停联合预警", "type": "联合预警"},
        {"id": "16", "name": "代谢综合征联合预警", "type": "联合预警 ⭐⭐⭐⭐⭐"},
        {"id": "17", "name": "呼吸衰竭风险联合预警", "type": "联合预警"},
        {"id": "18", "name": "心力衰竭风险联合预警", "type": "联合预警"},
        {"id": "19", "name": "低血糖昏迷风险联合预警", "type": "联合预警"},
        {"id": "20", "name": "高渗高血糖状态预警", "type": "联合预警"},
        {"id": "21", "name": "脓毒症风险联合预警", "type": "联合预警"},
        {"id": "22", "name": "心律失常猝死风险预警", "type": "联合预警"},
        {"id": "23", "name": "痛风风险联合预警", "type": "联合预警"},
        {"id": "24", "name": "脑卒中风险专项预警", "type": "专项预警 ⭐⭐⭐⭐⭐"},
        {"id": "25", "name": "心梗风险专项预警", "type": "专项预警 ⭐⭐⭐⭐⭐"}
    ]
    
    return {
        "total": len(models),
        "models": models,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.post("/api/v1/warning/generate", response_model=WarningResponse, tags=["预警服务"])
async def generate_warning_api(request: WarningRequest):
    """
    预警生成API
    核心接口：调用预警引擎生成预警 ⭐⭐⭐⭐⭐
    
    **流程：**
    1. 接收用户数据和模型ID
    2. 调用预警引擎（generate_warning）
    3. LangGraph强制验证闭环执行
    4. 返回预警结果 + 验证结果
    
    **预警分级：**
    - S级（红色紧急）：立即就医
    - A级（黄色高风险）：24h就医
    - B级（绿色中等）：本周复查
    - C级（白色低风险）：持续监测
    """
    try:
        # 调用核心引擎 ⭐⭐⭐⭐⭐
        result = generate_warning(
            user_id=request.user_id,
            model_id=request.model_id,
            input_data=request.input_data
        )
        
        return WarningResponse(
            warning_output=result["warning_output"],
            warning_level=result["warning_level"],
            validation_status=result["validation_status"],
            validation_score=result["validation_score"],
            retry_count=result.get("retry_count", 0)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"预警生成失败：{str(e)}"
        )

@app.get("/warning/levels", tags=["预警分级"])
async def get_warning_levels():
    """
    预警分级说明
    四级预警体系 ⭐⭐⭐⭐⭐
    """
    levels = [
        {
            "level": "S",
            "name": "紧急",
            "color": "红色",
            "response": "立即就医",
            "notification": ["App", "短信", "电话", "120"]
        },
        {
            "level": "A",
            "name": "高风险",
            "color": "黄色",
            "response": "24h就医",
            "notification": ["App", "短信"]
        },
        {
            "level": "B",
            "name": "中等",
            "color": "绿色",
            "response": "本周复查",
            "notification": ["App"]
        },
        {
            "level": "C",
            "name": "低风险",
            "color": "白色",
            "response": "持续监测",
            "notification": []
        }
    ]
    
    return {
        "total": len(levels),
        "levels": levels
    }

# ============================================
# 启动配置 ⭐⭐⭐⭐⭐
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )