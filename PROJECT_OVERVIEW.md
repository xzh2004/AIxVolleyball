# 📊 项目总览

排球AI训练系统 v3.0 - 完整技术文档

---

## 🎯 项目概述

### 项目定位
一个基于人工智能的排球垫球动作识别与训练系统，采用前后端分离的专业架构，为排球爱好者提供智能化的训练辅助。

### 核心价值
- **智能识别**: MediaPipe 33点姿态检测
- **科学评分**: 多维度量化评估系统
- **即时反馈**: AI驱动的个性化建议
- **游戏化**: 关卡系统激励学习
- **专业架构**: 易维护、可扩展

---

## 🏗️ 系统架构

### 三层架构设计

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│        (Streamlit Frontend)             │
│  ┌─────────┬─────────┬─────────────┐   │
│  │ Header  │ Upload  │ Score Card  │   │
│  └─────────┴─────────┴─────────────┘   │
└──────────────────┬──────────────────────┘
                   │ HTTP/Function Calls
┌──────────────────▼──────────────────────┐
│          API Layer                       │
│      (volleyball_api.py)                 │
│  ┌───────────────────────────────────┐  │
│  │  • analyze_uploaded_video()       │  │
│  │  • analyze_image()                │  │
│  │  • generate_visualization()       │  │
│  │  • get_score_summary()            │  │
│  └───────────────────────────────────┘  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Service Layer                      │
│   (volleyball_service.py)                │
│  ┌───────────────────────────────────┐  │
│  │  • Business Logic                 │  │
│  │  • Workflow Orchestration         │  │
│  │  • Data Processing                │  │
│  └───────────────────────────────────┘  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Core Layer                       │
│  ┌──────────┬──────────┬─────────────┐ │
│  │  Pose    │  Video   │   Scorer    │ │
│  │ Detector │Processor │             │ │
│  └──────────┴──────────┴─────────────┘ │
│  ┌──────────┬──────────┬─────────────┐ │
│  │Sequence  │Trajectory│   Video     │ │
│  │Analyzer  │Visualizer│  Generator  │ │
│  └──────────┴──────────┴─────────────┘ │
└─────────────────────────────────────────┘
```

### 模块职责

#### 1. Frontend Layer (前端层)
**位置**: `frontend/`

**职责**:
- 用户界面渲染
- 用户交互处理
- 数据展示和可视化

**组件**:
- `header.py`: 页面头部、关卡徽章
- `score_card.py`: 评分卡片、雷达图
- `video_uploader.py`: 视频上传、模式选择

#### 2. API Layer (接口层)
**位置**: `backend/api/`

**职责**:
- 对外接口定义
- 请求参数验证
- 响应格式标准化

**核心类**:
```python
class VolleyballAPI:
    def analyze_uploaded_video()    # 分析视频
    def analyze_image()             # 分析图像
    def generate_visualization()    # 生成可视化
    def get_score_summary()         # 获取评分摘要
```

#### 3. Service Layer (服务层)
**位置**: `backend/services/`

**职责**:
- 业务逻辑编排
- 多模块协调
- 复杂流程处理

**核心类**:
```python
class VolleyballService:
    def analyze_single_frame()      # 单帧分析
    def analyze_video()             # 视频分析
    def _analyze_video_sequence()   # 序列分析
    def generate_visualization_video() # 视频生成
```

#### 4. Core Layer (核心层)
**位置**: `backend/core/`

**职责**:
- 核心算法实现
- 底层功能封装
- 独立可测试

**模块**:
- `PoseDetector`: MediaPipe姿态检测
- `VideoProcessor`: 视频处理和帧提取
- `VolleyballScorer`: 动作评分算法
- `SequenceAnalyzer`: 连续帧分析
- `TrajectoryVisualizer`: 轨迹可视化
- `VideoGenerator`: 视频生成

---

## 📁 目录结构详解

```
volleyball-ai-training/
│
├── app.py                          # 🚀 主应用入口
│   ├── main()                      # 主函数
│   ├── render_analysis_page()      # 分析页面
│   ├── render_visualization_page() # 可视化页面
│   └── render_guide_page()         # 指南页面
│
├── backend/                        # 🔧 后端代码
│   ├── api/                       # API接口层
│   │   └── volleyball_api.py      # 主API类
│   ├── core/                      # 核心功能层
│   │   ├── pose_detector.py       # 姿态检测（MediaPipe）
│   │   ├── video_processor.py     # 视频处理（OpenCV）
│   │   ├── scorer.py              # 评分算法
│   │   ├── sequence_analyzer.py   # 序列分析
│   │   ├── trajectory_visualizer.py # 轨迹可视化
│   │   └── video_generator.py     # 视频生成
│   ├── services/                  # 业务逻辑层
│   │   └── volleyball_service.py  # 主服务类
│   ├── models/                    # 数据模型（预留）
│   └── utils/                     # 工具函数（预留）
│
├── frontend/                       # 🎨 前端代码
│   ├── components/                # UI组件
│   │   ├── header.py             # 页面头部
│   │   ├── score_card.py         # 评分展示
│   │   └── video_uploader.py     # 视频上传
│   ├── pages/                    # 页面（预留）
│   └── assets/                   # 静态资源（预留）
│
├── config/                        # ⚙️ 配置文件
│   ├── __init__.py
│   └── settings.py               # 系统配置
│       ├── MEDIAPIPE_CONFIG      # MediaPipe配置
│       ├── VIDEO_CONFIG          # 视频处理配置
│       ├── SCORING_CONFIG        # 评分配置
│       ├── LEVEL_CONFIG          # 关卡配置
│       └── STREAMLIT_CONFIG      # Streamlit配置
│
├── data/                          # 📦 数据目录
│   ├── models/                   # 模型文件
│   │   └── .gitkeep
│   └── templates/                # 动作模板
│       └── default_template.json # 标准动作模板
│
├── output/                        # 📤 输出目录
│   └── .gitkeep                  # 生成的视频等
│
├── tests/                         # 🧪 测试代码
│   ├── unit/                     # 单元测试
│   └── integration/              # 集成测试
│
├── requirements.txt               # 📋 依赖清单
├── .gitignore                    # 🚫 Git忽略文件
├── README.md                     # 📖 项目文档
├── QUICK_START.md                # 🚀 快速开始
├── MIGRATION_GUIDE.md            # 🔄 迁移指南
├── PROJECT_OVERVIEW.md           # 📊 本文件
├── run.bat                       # 🪟 Windows启动脚本
└── run.sh                        # 🐧 Linux/Mac启动脚本
```

---

## 🔍 核心算法

### 1. 姿态检测算法
**技术**: Google MediaPipe Pose

**流程**:
```
输入图像 
  → BlazePose检测
  → 33个关键点坐标
  → 归一化处理
  → 输出关键点字典
```

**关键点分布**:
- 面部: 0-10
- 躯干: 11-12 (肩膀), 23-24 (髋部)
- 上肢: 13-22 (肩、肘、腕、手指)
- 下肢: 25-32 (膝、踝、脚)

### 2. 评分算法
**多维度评分**:

#### 手臂评分 (40%)
```python
score = 基础分40
- abs(left_arm_angle - 165) * 惩罚系数
- abs(right_arm_angle - 165) * 惩罚系数
- abs(arm_gap - 25) * 惩罚系数
```

#### 身体评分 (30%)
```python
score = 基础分30
- abs(knee_angle - 75) * 惩罚系数
- abs(hip_height - 0.55) * 惩罚系数
```

#### 位置评分 (20%)
```python
score = 基础分20
- abs(arm_height - 0.45) * 惩罚系数
- abs(left_right_balance) * 惩罚系数
```

#### 稳定性评分 (10%)
```python
score = pose_confidence * 10
```

### 3. 序列分析算法

#### 流畅度评估
```python
smoothness = 1 / (1 + variance(angle_changes))
```

#### 完整性检测
```python
completeness = detected_frames / total_frames
```

#### 一致性评分
```python
consistency = 1 - abs(left_metrics - right_metrics)
```

---

## 🔌 API接口文档

### 核心API

#### 1. 分析上传视频
```python
def analyze_uploaded_video(uploaded_file, analysis_mode="single")
```

**参数**:
- `uploaded_file`: Streamlit文件对象
- `analysis_mode`: "single" | "sequence"

**返回**:
```python
{
    "success": True,
    "landmarks": {...},
    "score": {...},
    "pose_image": ndarray,
    "video_info": {...},
    "analysis_mode": "single_frame"
}
```

#### 2. 分析图像
```python
def analyze_image(image)
```

**参数**:
- `image`: numpy array or PIL Image

**返回**:
```python
{
    "success": True,
    "landmarks": {...},
    "score": {...},
    "pose_image": ndarray
}
```

#### 3. 生成可视化
```python
def generate_visualization(uploaded_file, vis_type="overlay")
```

**参数**:
- `uploaded_file`: 视频文件
- `vis_type`: "overlay" | "skeleton" | "comparison" | "trajectory"

**返回**:
```python
(success: bool, output_path: str, error: str)
```

#### 4. 获取评分摘要
```python
def get_score_summary(score_result)
```

**返回**:
```python
{
    "total_score": 85,
    "arm_score": 35,
    "body_score": 25,
    "position_score": 18,
    "stability_score": 7,
    "level_info": {...},
    "feedback": [...]
}
```

---

## 🎨 前端组件说明

### 1. Header组件
**文件**: `frontend/components/header.py`

**功能**:
- 渲染页面顶部横幅
- 显示关卡徽章
- 响应式设计

**使用**:
```python
from frontend.components.header import render_header
render_header()
```

### 2. ScoreCard组件
**文件**: `frontend/components/score_card.py`

**功能**:
- 总分大屏展示
- 分项得分metrics
- 雷达图可视化
- 反馈建议列表

**使用**:
```python
from frontend.components.score_card import render_score_card
render_score_card(score_summary)
```

### 3. VideoUploader组件
**文件**: `frontend/components/video_uploader.py`

**功能**:
- 视频文件上传
- 分析模式选择
- 可视化类型选择

**使用**:
```python
from frontend.components.video_uploader import render_video_uploader
uploaded_file = render_video_uploader()
```

---

## ⚙️ 配置说明

### MediaPipe配置
```python
MEDIAPIPE_CONFIG = {
    "static_image_mode": False,      # 视频模式
    "model_complexity": 1,           # 模型复杂度(0-2)
    "smooth_landmarks": True,        # 平滑关键点
    "min_detection_confidence": 0.5, # 检测置信度
    "min_tracking_confidence": 0.5   # 跟踪置信度
}
```

### 视频处理配置
```python
VIDEO_CONFIG = {
    "max_file_size_mb": 50,          # 最大文件大小
    "supported_formats": [".mp4", ...], # 支持格式
    "frame_extraction_fps": 2,       # 帧提取FPS
    "max_duration_seconds": 30       # 最大时长
}
```

### 评分配置
```python
SCORING_CONFIG = {
    "weights": {
        "arm_score": 0.4,      # 40%
        "body_score": 0.3,     # 30%
        "position_score": 0.2,  # 20%
        "stability_score": 0.1  # 10%
    },
    "passing_score": 60,
    "excellent_score": 85
}
```

---

## 🧪 测试策略

### 单元测试
**位置**: `tests/unit/`

**覆盖**:
- 姿态检测功能
- 评分算法逻辑
- 视频处理函数
- 工具函数

### 集成测试
**位置**: `tests/integration/`

**覆盖**:
- API接口调用
- 服务层业务流程
- 端到端功能测试

### 测试运行
```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成覆盖率报告
pytest --cov=backend --cov=frontend
```

---

## 🚀 部署方案

### 本地部署
```bash
streamlit run app.py
```

### Docker部署（预留）
```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### 云部署选项
- Streamlit Cloud（推荐）
- Heroku
- AWS EC2
- Google Cloud Platform

---

## 📈 性能指标

### 处理速度
- 单帧分析: ~3秒
- 序列分析: ~10秒
- 视频生成: ~20-30秒

### 准确率
- 姿态检测: >95% (MediaPipe)
- 评分精度: 参考标准动作模板
- 关键点识别: 33点全覆盖

---

## 🔐 安全考虑

### 数据安全
- 所有上传视频存储在临时目录
- 处理完成后自动清理
- 不进行云端存储

### 隐私保护
- 本地处理，不上传服务器
- 无用户数据收集
- 开源透明

---

## 🛣️ 未来规划

### v3.1 计划
- [ ] 增加更多排球动作（扣球、发球）
- [ ] 多人协同训练模式
- [ ] 历史记录和进度追踪
- [ ] 移动端适配

### v4.0 愿景
- [ ] 3D姿态重建
- [ ] VR/AR训练模式
- [ ] 社交和排行榜
- [ ] AI教练对话系统

---

## 📚 参考资料

### 技术文档
- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenCV Documentation](https://docs.opencv.org/)

### 排球训练资源
- 排球基础技术教学
- 标准动作视频示范
- 体育科学研究论文

---

**更新日期**: 2025-10-31  
**版本**: v3.0.0  
**维护者**: Volleyball AI Training Team

