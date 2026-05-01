"""
数据分析模块
健康趋势分析 + 预警历史统计 + 数据可视化

创建时间：2026-05-01 19:47
版本：v1.0
开发者：匠心Agent + 格物Agent
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

# ============================================
# 健康趋势分析 ⭐⭐⭐⭐⭐
# ============================================

class HealthTrendAnalyzer:
    """健康趋势分析器"""
    
    def __init__(self):
        self.name = "健康趋势分析器"
    
    def analyze_blood_pressure_trend(
        self,
        health_records: List[Dict],
        days: int = 30
    ) -> Dict:
        """
        分析血压趋势
        
        Args:
            health_records: 健康记录列表
            days: 分析天数
        
        Returns:
            Dict: 血压趋势分析结果
        """
        # 提取血压数据
        bp_records = [
            r for r in health_records
            if r["data_type"] == "blood_pressure"
        ]
        
        if len(bp_records) < 2:
            return {"trend": "insufficient_data", "message": "数据不足"}
        
        # 解析数据
        sbp_values = []
        dbp_values = []
        
        for record in bp_records[:days]:
            data_value = json.loads(record["data_value"])
            sbp_values.append(data_value.get("sbp_value", 0))
            dbp_values.append(data_value.get("dbp_value", 0))
        
        # 计算平均值
        avg_sbp = sum(sbp_values) / len(sbp_values)
        avg_dbp = sum(dbp_values) / len(dbp_values)
        
        # 计算趋势（简单线性）
        sbp_trend = "stable"  # 稳定
        if len(sbp_values) >= 7:
            recent_avg = sum(sbp_values[-7:]) / 7
            early_avg = sum(sbp_values[:7]) / 7
            if recent_avg > early_avg + 5:
                sbp_trend = "rising"  # 上升 ⭐⭐⭐⭐⭐
            elif recent_avg < early_avg - 5:
                sbp_trend = "declining"  #下降
        
        return {
            "avg_sbp": round(avg_sbp, 1),
            "avg_dbp": round(avg_dbp, 1),
            "sbp_trend": sbp_trend,
            "record_count": len(bp_records),
            "analysis_period_days": days
        }
    
    def analyze_glucose_trend(
        self,
        health_records: List[Dict],
        days: int = 30
    ) -> Dict:
        """
        分析血糖趋势
        
        Args:
            health_records: 健康记录列表
            days: 分析天数
        
        Returns:
            Dict: 血糖趋势分析结果
        """
        # 提取血糖数据
        glucose_records = [
            r for r in health_records
            if r["data_type"] == "glucose"
        ]
        
        if len(glucose_records) < 2:
            return {"trend": "insufficient_data", "message": "数据不足"}
        
        # 解析数据
        glucose_values = []
        
        for record in glucose_records[:days]:
            data_value = json.loads(record["data_value"])
            glucose_values.append(data_value.get("glucose_value", 0))
        
        # 计算平均值
        avg_glucose = sum(glucose_values) / len(glucose_values)
        
        # 计算趋势
        glucose_trend = "stable"
        if len(glucose_values) >= 7:
            recent_avg = sum(glucose_values[-7:]) / 7
            early_avg = sum(glucose_values[:7]) / 7
            if recent_avg > early_avg + 1.0:
                glucose_trend = "rising"  # 上升 ⭐⭐⭐⭐⭐
            elif recent_avg < early_avg - 1.0:
                glucose_trend = "declining"  #下降
        
        # 计算达标率（目标范围：4.4-7.0 mmol/L）
        target_count = len([v for v in glucose_values if 4.4 <= v <= 7.0])
        target_rate = target_count / len(glucose_values) * 100
        
        return {
            "avg_glucose": round(avg_glucose, 1),
            "glucose_trend": glucose_trend,
            "target_rate": round(target_rate, 1),
            "record_count": len(glucose_records),
            "analysis_period_days": days
        }

# ============================================
# 预警统计分析 ⭐⭐⭐⭐⭐
# ============================================

class WarningStatisticsAnalyzer:
    """预警统计分析器"""
    
    def __init__(self):
        self.name = "预警统计分析器"
    
    def analyze_warning_distribution(
        self,
        warning_history: List[Dict]
    ) -> Dict:
        """
        分析预警分布
        
        Args:
            warning_history: 预警历史列表
        
        Returns:
            Dict: 预警分布统计
        """
        if len(warning_history) == 0:
            return {"total": 0, "message": "无预警记录"}
        
        # 统计各等级预警数量
        s_count = len([w for w in warning_history if w["warning_level"] == "S"])
        a_count = len([w for w in warning_history if w["warning_level"] == "A"])
        b_count = len([w for w in warning_history if w["warning_level"] == "B"])
        c_count = len([w for w in warning_history if w["warning_level"] == "C"])
        
        total = len(warning_history)
        
        # 计算占比
        distribution = {
            "total": total,
            "S_level": {
                "count": s_count,
                "percentage": round(s_count / total * 100, 1) if total > 0 else 0
            },
            "A_level": {
                "count": a_count,
                "percentage": round(a_count / total * 100, 1) if total > 0 else 0
            },
            "B_level": {
                "count": b_count,
                "percentage": round(b_count / total * 100, 1) if total > 0 else 0
            },
            "C_level": {
                "count": c_count,
                "percentage": round(c_count / total * 100, 1) if total > 0 else 0
            }
        }
        
        return distribution
    
    def analyze_warning_frequency(
        self,
        warning_history: List[Dict],
        days: int = 30
    ) -> Dict:
        """
        分析预警频率
        
        Args:
            warning_history: 预警历史列表
            days: 分析天数
        
        Returns:
            Dict: 预警频率统计
        """
        if len(warning_history) == 0:
            return {"frequency": 0, "message": "无预警记录"}
        
        # 按日期分组统计
        date_count = {}
        
        for warning in warning_history:
            warning_time = warning.get("warning_time", "")
            if warning_time:
                date = warning_time.split()[0]  # 提取日期部分
                date_count[date] = date_count.get(date, 0) + 1
        
        # 计算平均频率
        total_days = len(date_count) if date_count else 1
        avg_frequency = len(warning_history) / total_days
        
        # 计算高频预警天数
        high_frequency_days = len([d for d, c in date_count.items() if c >= 3])
        
        return {
            "avg_frequency": round(avg_frequency, 2),
            "total_warnings": len(warning_history),
            "high_frequency_days": high_frequency_days,
            "analysis_period_days": days
        }

# ============================================
# 数据可视化接口 ⭐⭐⭐⭐⭐
# ============================================

class DataVisualizationGenerator:
    """数据可视化生成器"""
    
    @staticmethod
    def generate_bp_chart_data(
        health_records: List[Dict],
        days: int = 30
    ) -> Dict:
        """
        生成血压图表数据
        
        Args:
            health_records: 健康记录列表
            days: 分析天数
        
        Returns:
            Dict: 图表数据
        """
        bp_records = [
            r for r in health_records
            if r["data_type"] == "blood_pressure"
        ][:days]
        
        chart_data = {
            "title": "血压趋势图",
            "xAxis": [],
            "series": [
                {"name": "收缩压", "data": []},
                {"name": "舒张压", "data": []}
            ]
        }
        
        for record in bp_records:
            data_value = json.loads(record["data_value"])
            chart_data["xAxis"].append(record["data_time"].split()[0])
            chart_data["series"][0]["data"].append(data_value.get("sbp_value", 0))
            chart_data["series"][1]["data"].append(data_value.get("dbp_value", 0))
        
        return chart_data
    
    @staticmethod
    def generate_warning_pie_data(
        warning_history: List[Dict]
    ) -> Dict:
        """
        生成预警饼图数据
        
        Args:
            warning_history: 预警历史列表
        
        Returns:
            Dict: 饼图数据
        """
        s_count = len([w for w in warning_history if w["warning_level"] == "S"])
        a_count = len([w for w in warning_history if w["warning_level"] == "A"])
        b_count = len([w for w in warning_history if w["warning_level"] == "B"])
        c_count = len([w for w in warning_history if w["warning_level"] == "C"])
        
        pie_data = {
            "title": "预警等级分布",
            "series": [
                {"name": "S级", "value": s_count, "color": "#e74c3c"},
                {"name": "A级", "value": a_count, "color": "#f39c12"},
                {"name": "B级", "value": b_count, "color": "#27ae60"},
                {"name": "C级", "value": c_count, "color": "#95a5a6"}
            ]
        }
        
        return pie_data

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

def analyze_health_trend_api(
    health_records: List[Dict],
    data_type: str = "blood_pressure",
    days: int = 30
) -> Dict:
    """
    健康趋势分析API
    
    Args:
        health_records: 健康记录列表
        data_type: 数据类型
        days: 分析天数
    
    Returns:
        Dict: 趋势分析结果
    """
    analyzer = HealthTrendAnalyzer()
    
    if data_type == "blood_pressure":
        result = analyzer.analyze_blood_pressure_trend(health_records, days)
    elif data_type == "glucose":
        result = analyzer.analyze_glucose_trend(health_records, days)
    else:
        result = {"error": "不支持的数据类型"}
    
    return result

def analyze_warning_stats_api(
    warning_history: List[Dict],
    days: int = 30
) -> Dict:
    """
    预警统计分析API
    
    Args:
        warning_history: 预警历史列表
        days: 分析天数
    
    Returns:
        Dict: 统计分析结果
    """
    analyzer = WarningStatisticsAnalyzer()
    
    distribution = analyzer.analyze_warning_distribution(warning_history)
    frequency = analyzer.analyze_warning_frequency(warning_history, days)
    
    return {
        "distribution": distribution,
        "frequency": frequency
    }

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("数据分析模块测试")
    print("=" * 60)
    
    # 测试血压趋势分析
    test_records = [
        {
            "data_type": "blood_pressure",
            "data_value": '{"sbp_value": 135, "dbp_value": 88}',
            "data_time": "2026-05-01 08:00:00"
        },
        {
            "data_type": "blood_pressure",
            "data_value": '{"sbp_value": 140, "dbp_value": 90}',
            "data_time": "2026-05-02 08:00:00"
        }
    ]
    
    result = analyze_health_trend_api(test_records, "blood_pressure")
    print(f"血压趋势分析结果：{result}")
    
    print("=" * 60)