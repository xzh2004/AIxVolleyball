"""
项目配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = DATA_DIR / "models"
TEMPLATES_DIR = DATA_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"

# 确保目录存在
for dir_path in [DATA_DIR, MODELS_DIR, TEMPLATES_DIR, OUTPUT_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# MediaPipe 配置
MEDIAPIPE_CONFIG = {
    "static_image_mode": False,
    "model_complexity": 1,
    "smooth_landmarks": True,
    "enable_segmentation": False,
    "smooth_segmentation": True,
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5
}

# 视频处理配置
VIDEO_CONFIG = {
    "max_file_size_mb": 50,
    "supported_formats": [".mp4", ".avi", ".mov", ".mkv"],
    "frame_extraction_fps": 2,  # 每秒提取帧数
    "max_duration_seconds": 30
}

# 评分配置
SCORING_CONFIG = {
    "weights": {
        "arm_score": 0.4,      # 40%
        "body_score": 0.3,     # 30%
        "position_score": 0.2,  # 20%
        "stability_score": 0.1  # 10%
    },
    "passing_score": 60,  # 及格分数
    "excellent_score": 85  # 优秀分数
}

# 标准动作模板（默认值）
DEFAULT_TEMPLATE = {
    "arm_angle": 165,        # 手臂伸直角度
    "arm_gap_angle": 25,     # 双臂夹角
    "knee_angle": 75,        # 膝盖弯曲角度
    "hip_height": 0.55,      # 髋部相对高度
    "arm_height": 0.45,      # 手臂触球高度
    "description": "标准排球垫球姿态模板"
}

# 游戏关卡配置
LEVEL_CONFIG = {
    "beginner": {
        "name": "初级",
        "passing_score": 50,
        "description": "基础垫球动作"
    },
    "intermediate": {
        "name": "中级",
        "passing_score": 70,
        "description": "标准垫球动作"
    },
    "advanced": {
        "name": "高级",
        "passing_score": 85,
        "description": "专业垫球动作"
    }
}

# API 配置
API_CONFIG = {
    "host": "localhost",
    "port": 8000,
    "debug": True,
    "cors_origins": ["*"]
}

# Streamlit 配置
STREAMLIT_CONFIG = {
    "page_title": "🏐 排球AI训练系统",
    "page_icon": "🏐",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

