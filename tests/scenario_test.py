"""
家庭健康预警系统场景验证测试
Phase 1开发 - 用户原型验证

创建时间：2026-05-01 16:30
版本：v1.0
验证者：明镜Agent
"""

import sys
sys.path.append('/Users/lizhihua/.openclaw/workspace/family_health_warning_system')

from core.engine import generate_warning
from datetime import datetime

# ============================================
# 场景1：张阿姨（DKA预警）⭐⭐⭐⭐⭐
# ============================================

def test_zhang_aunt_dka():
    """
    场景1：张阿姨 - DKA预警（S级）
    
    数据来源：血糖仪 + 血酮仪
    场景：早晨测血糖15.0mmol/L + 血酮3.5mmol/L
    预期：S级预警（紧急）
    """
    print("=" * 70)
    print("场景1：张阿姨 - DKA预警测试 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    # 测试数据
    result = generate_warning(
        user_id="zhang_aunt_001",
        model_id="12",  # DKA预警模型
        input_data={
            "glucose_value": 15.0,  # 高血糖
            "ketone_value": 3.5,    # 高血酮
            "data_verified": True,
            "data_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
    # 输出结果
    print(f"预警等级：{result['warning_level']}")
    print(f"验证状态：{result['validation_status']}")
    print(f"验证评分：{result['validation_score']}")
    
    if result['warning_output']:
        print(f"预警说明：{result['warning_output'].get('explanation')}")
        print(f"建议措施：{result['warning_output'].get('suggestion')}")
        print(f"循证依据：{result['warning_output'].get('evidence')}")
    
    # 明镜验证 ⭐⭐⭐⭐⭐
    print("\n[明镜验证] try to break it")
    print("-" * 70)
    
    # 检查预警等级
    if result['warning_level'] != "S":
        print("❌ 验证失败：预警等级应为S级（紧急）")
        return False
    else:
        print("✅ 验证通过：预警等级正确（S级）")
    
    # 检查验证状态
    if result['validation_status'] != "pass":
        print("❌ 验证失败：验证状态应为pass")
        return False
    else:
        print("✅ 验证通过：验证状态正确（pass）")
    
    # 检查验证评分
    if result['validation_score'] < 80:
        print("❌ 验证失败：验证评分应≥80")
        return False
    else:
        print("✅ 验证通过：验证评分合格")
    
    # 检查建议措施 ⭐⭐⭐⭐⭐
    if result['warning_output']:
        suggestion = result['warning_output'].get('suggestion', [])
        if "就医" not in str(suggestion):
            print("❌ 验证失败：S级必须建议就医")
            return False
        else:
            print("✅ 验证通过：建议措施合理")
    
    print("=" * 70)
    print("场景1验证结果：✅ 通过 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    return True

# ============================================
# 场景2：王大爷（房颤预警）⭐⭐⭐⭐⭐
# ============================================

def test_wang_grandpa_afib():
    """
    场景2：王大爷 - 房颤预警（S级）
    
    数据来源：智能手表（心电监测）
    场景：夜间检测到房颤 + 心率110次/分
    预期：S级预警（紧急）
    """
    print("\n" + "=" * 70)
    print("场景2：王大爷 - 房颤预警测试 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    # 测试数据
    result = generate_warning(
        user_id="wang_grandpa_001",
        model_id="04",  # 心电预警模型
        input_data={
            "rhythm_type": "房颤",  # 检测到房颤 ⭐⭐⭐⭐⭐
            "heart_rate": 110,    # 心率110
            "arrhythmia_count": 5,  # 心律失常次数 ⭐⭐⭐⭐⭐
            "data_verified": True,
            "data_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
    # 输出结果
    print(f"预警等级：{result['warning_level']}")
    print(f"验证状态：{result['validation_status']}")
    print(f"验证评分：{result['validation_score']}")
    
    # 明镜验证 ⭐⭐⭐⭐⭐
    print("\n[明镜验证] try to break it")
    print("-" * 70)
    
    # 检查预警等级
    if result['warning_level'] != "S":
        print("❌ 验证失败：预警等级应为S级（紧急）")
        return False
    else:
        print("✅ 验证通过：预警等级正确（S级）")
    
    # 检查验证状态
    if result['validation_status'] != "pass":
        print("❌ 验证失败：验证状态应为pass")
        return False
    else:
        print("✅ 验证通过：验证状态正确（pass）")
    
    print("=" * 70)
    print("场景2验证结果：✅ 通过 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    return True

# ============================================
# 场景3：李先生（代谢综合征）⭐⭐⭐⭐⭐
# ============================================

def test_li_mr_metabolic():
    """
    场景3：李先生 - 代谢综合征预警（A级）
    
    数据来源：智能手表 + 体重秤
    场景：血压135/88 + 血糖5.8 + BMI 26.5 + TG 1.8
    预期：A级预警（高风险）
    """
    print("\n" + "=" * 70)
    print("场景3：李先生 - 代谢综合征预警测试 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    # 测试数据
    result = generate_warning(
        user_id="li_mr_001",
        model_id="16",  # 代谢综合征预警模型
        input_data={
            "sbp_value": 135,  # 收缩压 ⭐⭐⭐⭐⭐
            "dbp_value": 88,   # 舒张压 ⭐⭐⭐⭐⭐
            "fbg_value": 5.8,  # 空腹血糖 ⭐⭐⭐⭐⭐
            "bmi_value": 26.5,
            "tg_value": 1.8,
            "hdl_value": 1.0,  # HDL胆固醇 ⭐⭐⭐⭐⭐
            "data_verified": True,
            "data_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
    # 输出结果
    print(f"预警等级：{result['warning_level']}")
    print(f"验证状态：{result['validation_status']}")
    print(f"验证评分：{result['validation_score']}")
    
    # 明镜验证 ⭐⭐⭐⭐⭐
    print("\n[明镜验证] try to break it")
    print("-" * 70)
    
    # 检查预警等级
    if result['warning_level'] not in ["A", "B"]:
        print("❌ 验证失败：预警等级应为A级或B级")
        return False
    else:
        print("✅ 验证通过：预警等级正确")
    
    # 检查验证状态
    if result['validation_status'] != "pass":
        print("❌ 验证失败：验证状态应为pass")
        return False
    else:
        print("✅ 验证通过：验证状态正确（pass）")
    
    print("=" * 70)
    print("场景3验证结果：✅ 通过 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    return True

# ============================================
# 全场景验证 ⭐⭐⭐⭐⭐
# ============================================

def run_all_scenario_tests():
    """
    执行所有场景验证测试
    """
    print("\n" + "=" * 70)
    print("家庭健康预警系统 - 全场景验证测试 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    print(f"测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = []
    
    # 场景1：张阿姨
    results.append(("张阿姨-DKA", test_zhang_aunt_dka()))
    
    # 场景2：王大爷
    results.append(("王大爷-房颤", test_wang_grandpa_afib()))
    
    # 场景3：李先生
    results.append(("李先生-代谢综合征", test_li_mr_metabolic()))
    
    # 总结
    print("\n" + "=" * 70)
    print("验证测试总结 ⭐⭐⭐⭐⭐")
    print("=" * 70)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    # 统计
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print("=" * 70)
    print(f"通过率：{passed_count}/{total_count} ({passed_count/total_count*100:.1f}%)")
    print("=" * 70)
    
    if passed_count == total_count:
        print("\n✅ 全场景验证通过！ ⭐⭐⭐⭐⭐")
        print("Phase 1开发验证成功！")
    else:
        print("\n❌ 存在验证失败场景")
        print("需要修复问题后重新验证")
    
    return passed_count == total_count

# ============================================
# 主入口
# ============================================

if __name__ == "__main__":
    run_all_scenario_tests()