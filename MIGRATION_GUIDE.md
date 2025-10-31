# 🔄 迁移指南 - v3.0

从旧版本迁移到v3.0的模块化架构

---

## 📋 主要变化

### 1. 目录结构重组

#### 旧结构 → 新结构

| 旧文件 | 新位置 | 说明 |
|--------|--------|------|
| `pose_detector.py` | `backend/core/pose_detector.py` | 核心模块 |
| `video_processor.py` | `backend/core/video_processor.py` | 核心模块 |
| `scorer.py` | `backend/core/scorer.py` | 核心模块 |
| `sequence_analyzer.py` | `backend/core/sequence_analyzer.py` | 核心模块 |
| `trajectory_visualizer.py` | `backend/core/trajectory_visualizer.py` | 核心模块 |
| `video_generator.py` | `backend/core/video_generator.py` | 核心模块 |
| `template.json` | `data/templates/default_template.json` | 数据文件 |
| `app.py` | `app.py` (全新重写) | 主应用 |

### 2. 架构变化

```
旧架构:
app.py → 直接调用各个模块

新架构:
app.py → API层 → 服务层 → 核心模块层
```

### 3. 导入方式变化

#### 旧导入方式
```python
from pose_detector import PoseDetector
from scorer import VolleyballScorer
```

#### 新导入方式
```python
from backend.api import VolleyballAPI

# 或者直接使用服务层
from backend.services import VolleyballService

# 或者使用核心模块
from backend.core import PoseDetector, VolleyballScorer
```

---

## 🚀 迁移步骤

### 步骤1: 备份旧文件（可选）

```bash
# 创建备份目录
mkdir backup_v2
# 复制旧文件
xcopy *.py backup_v2\
```

### 步骤2: 使用新架构

新架构已经自动集成，你只需要：

```bash
# 1. 确保依赖已安装
pip install -r requirements.txt

# 2. 直接运行新版本
streamlit run app.py

# 或使用启动脚本
# Windows:
run.bat

# Linux/Mac:
chmod +x run.sh
./run.sh
```

### 步骤3: 迁移自定义代码（如果有）

如果你修改过原代码，需要将修改迁移到新结构：

#### 3.1 修改了核心模块
将修改应用到 `backend/core/` 对应文件

#### 3.2 修改了评分逻辑
将修改应用到 `backend/core/scorer.py`

#### 3.3 添加了新功能
- 核心功能 → `backend/core/`
- 业务逻辑 → `backend/services/`
- API接口 → `backend/api/`
- UI组件 → `frontend/components/`

### 步骤4: 测试新系统

```bash
# 运行应用
streamlit run app.py

# 测试以下功能:
# 1. 上传视频
# 2. 单帧分析
# 3. 连续帧分析
# 4. 视频可视化
```

---

## 🔍 常见问题

### Q1: 旧文件还能用吗？

**A**: 可以。旧文件（`pose_detector.py`, `scorer.py`等）仍然在项目根目录，不会被删除。新系统使用的是`backend/core/`下的副本。

### Q2: 如何使用旧的独立脚本？

**A**: 如果你有使用旧模块的自定义脚本：

```python
# 选项1: 继续使用根目录的旧文件（不推荐）
from pose_detector import PoseDetector

# 选项2: 更新导入路径（推荐）
from backend.core import PoseDetector
```

### Q3: 配置文件在哪里？

**A**: 所有配置已移至 `config/settings.py`，你可以在这里修改：
- MediaPipe参数
- 视频处理参数
- 评分权重
- 关卡设置
等

### Q4: 如何修改评分标准？

**A**: 编辑以下文件：
1. `config/settings.py` - 修改权重和阈值
2. `data/templates/default_template.json` - 修改标准动作模板
3. `backend/core/scorer.py` - 修改评分算法

### Q5: 如何添加新的分析模式？

**A**: 
1. 在 `backend/core/` 添加核心功能
2. 在 `backend/services/volleyball_service.py` 添加业务逻辑
3. 在 `backend/api/volleyball_api.py` 暴露API
4. 在 `app.py` 添加UI界面

---

## 📊 新旧对比

| 特性 | 旧版本 | 新版本 v3.0 |
|------|--------|-------------|
| 架构 | 单层，文件散乱 | 三层架构，模块化 |
| 代码组织 | 所有文件在根目录 | 清晰的目录结构 |
| 前后端 | 耦合在一起 | 完全分离 |
| 可维护性 | 较难维护 | 易于维护和扩展 |
| UI设计 | 基础Streamlit | 现代化专业UI |
| 文档 | 基础README | 完整文档体系 |
| 配置管理 | 硬编码 | 集中配置文件 |

---

## ✅ 迁移检查清单

- [ ] 安装新依赖 `pip install -r requirements.txt`
- [ ] 确认模板文件在 `data/templates/` 目录
- [ ] 运行新应用 `streamlit run app.py`
- [ ] 测试视频上传功能
- [ ] 测试单帧分析
- [ ] 测试连续帧分析
- [ ] 测试视频可视化
- [ ] （可选）迁移自定义修改
- [ ] （可选）备份或清理旧文件

---

## 🎯 后续建议

### 清理旧文件（可选）

一旦确认新系统运行正常，可以考虑清理根目录的旧文件：

```bash
# 保留但移到old_version目录
mkdir old_version
move pose_detector.py old_version\
move video_processor.py old_version\
move scorer.py old_version\
move sequence_analyzer.py old_version\
move trajectory_visualizer.py old_version\
move video_generator.py old_version\
move quick_test.py old_version\
move test_generate_all.py old_version\
```

### 学习新架构

建议阅读：
1. `README.md` - 完整项目文档
2. `config/settings.py` - 了解配置选项
3. `backend/api/volleyball_api.py` - 了解API接口
4. `backend/services/volleyball_service.py` - 了解业务逻辑

---

## 💡 获取帮助

如果迁移过程中遇到问题：

1. 查看 `README.md` 完整文档
2. 检查 `config/settings.py` 配置
3. 查看控制台错误信息
4. 提交 GitHub Issue

---

**祝你使用愉快！🏐**

