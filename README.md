# 家庭健康预警服务系统

基于25个预警模型的多维度健康预警平台，集成LangGraph强制验证闭环。

## 核心功能

- ✅ 25个预警模型（11个单项 + 12个联合 + 2个专项）
- ✅ LangGraph强制验证闭环
- ✅ FastAPI服务
- ✅ 四级预警体系（S/A/B/C）

## 项目结构

```
family_health_warning_system/
├── core/
│   ├── engine.py          # LangGraph核心引擎
│   ├── validator.py       # 明镜验证器
│   └── __init__.py
├── models/
│   ├── warning_models.py  # 25个预警模型
│   └── __init__.py
├── api/
│   ├── main.py            # FastAPI服务
│   └── __init__.py
├── tests/
│   ├── scenario_test.py   # 场景验证测试
│   └── 验证说明.md
├── requirements.txt       # 依赖包
└── README.md              # 说明文档
```

## API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/warning/generate` | POST | 预警生成API |
| `/health` | GET | 健康检查 |
| `/models/list` | GET | 25个模型清单 |
| `/docs` | GET | Swagger UI |

## 预警分级

| 级别 | 颜色 | 说明 | 响应机制 |
|------|------|------|---------|
| **S级** | 🔴 红色 | 紧急风险 | 立即就医 |
| **A级** | 🟡 黄色 | 高风险 | 24h就医 |
| **B级** | 🟢 绿色 | 中等风险 | 本周复查 |
| **C级** | ⚪ 白色 | 低风险 | 持续监测 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/family_health_warning_system.git

# 安装依赖
pip install -r requirements.txt

# 启动API服务
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## 测试

```bash
# 运行场景验证测试
python tests/scenario_test.py
```

## 技术栈

- **Python 3.14**
- **FastAPI 0.136**
- **LangGraph**
- **Pydantic 2.13**

## 开发进度

| Phase | 完成度 |
|-------|--------|
| **Phase 1** | ✅ 100% |
| **核心引擎** | ✅ 完成 |
| **验证闭环** | ✅ 完成 |
| **API服务** | ✅ 完成 |

## 作者

**匠心Agent + 磐石Agent + 天工Agent + 明镜Agent**

## 许可证

MIT License