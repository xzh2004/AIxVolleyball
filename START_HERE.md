# 🏐 开始使用 - 排球AI训练系统 v3.0

欢迎使用全新的模块化排球AI训练系统！

---

## 🎉 项目重构完成！

你现在拥有一个**专业的、模块化的、前后端分离**的排球动作识别系统。

---

## 🚀 立即开始（3步）

### 步骤 1: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 1.5: 安装FFmpeg（推荐）
为了视频能在浏览器中播放：
```bash
conda install ffmpeg
```
详见 [INSTALL_FFMPEG.md](INSTALL_FFMPEG.md)

### 步骤 2: 启动应用
```bash
# 方式1: 使用启动脚本（推荐）
run.bat

# 方式2: 直接运行
streamlit run app.py
```

### 步骤 3: 开始使用
- 浏览器自动打开 http://localhost:8501
- 上传你的垫球视频
- 查看AI分析结果！

---

## 📚 重要文档

### 新手必读
1. **[QUICK_START.md](QUICK_START.md)** ⭐
   - 5分钟快速上手指南
   - 详细使用教程
   - 常见问题解答

2. **[README.md](README.md)**
   - 完整项目文档
   - 功能介绍
   - 技术栈说明

### 开发者文档
3. **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** ⭐⭐⭐
   - 系统架构详解
   - API接口文档
   - 核心算法说明

4. **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)**
   - 从旧版本迁移指南
   - 代码组织变化
   - 导入方式更新

### 重构总结
5. **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** ⭐
   - 重构完成总结
   - 新建文件清单
   - 主要改进说明

---

## 🎯 核心功能

### 1️⃣ 动作分析
- **单帧快速分析**: 3秒出结果
- **连续帧深度分析**: 流畅度、完整性、一致性评估
- **多维度评分**: 手臂、身体、位置、稳定性
- **智能反馈**: AI驱动的个性化建议

### 2️⃣ 视频可视化
- 🎥 骨架叠加 - 最直观
- 🦴 纯骨架动画 - 最清晰（**最快**）
- 📊 左右对比 - 最专业
- 📈 轨迹追踪 - 最动感

⚠️ **重要提示**: 视频生成需要对每帧进行AI分析，**需要30秒-2分钟**，请耐心等待。
- 推荐使用3-10秒的短视频
- 从命令行启动可看到进度
- **强烈推荐安装FFmpeg**以在浏览器中直接播放视频
- 详见 [VIDEO_GENERATION_GUIDE.md](VIDEO_GENERATION_GUIDE.md) 和 [INSTALL_FFMPEG.md](INSTALL_FFMPEG.md)

### 3️⃣ 游戏化系统
- 🌱 初级关卡 (50分)
- 🌟 中级关卡 (70分)
- 🏆 高级关卡 (85分)

---

## 📁 新项目结构

```
volleyball-ai-training/
├── app.py                     # 🚀 主应用入口
├── backend/                   # 🔧 后端代码
│   ├── api/                  # API接口层
│   ├── core/                 # 核心功能层
│   └── services/             # 业务逻辑层
├── frontend/                  # 🎨 前端代码
│   └── components/           # UI组件
├── config/                    # ⚙️ 配置文件
│   └── settings.py           # 系统配置
├── data/                      # 📦 数据文件
│   └── templates/            # 动作模板
└── output/                    # 📤 输出文件
```

---

## 🔍 快速导航

### 想要了解...

**如何使用系统？**
→ 阅读 [QUICK_START.md](QUICK_START.md)

**系统如何工作？**
→ 阅读 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

**如何修改配置？**
→ 编辑 [config/settings.py](config/settings.py)

**如何添加新功能？**
→ 查看 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) 的"添加新功能"章节

**遇到问题怎么办？**
→ 查看 [QUICK_START.md](QUICK_START.md) 的"常见问题"章节

---

## ⚡ 快速测试

### 测试视频要求
- **格式**: MP4, AVI, MOV, MKV
- **时长**: 3-10秒
- **角度**: 正面拍摄，全身入镜
- **大小**: ≤ 50MB

### 测试步骤
1. 启动系统：`streamlit run app.py`
2. 点击"动作分析"
3. 上传测试视频
4. 选择"单帧分析"
5. 点击"开始分析"
6. 查看结果！

---

## 💡 核心优势

### ✨ 架构升级
- **前后端分离**: 清晰的职责划分
- **三层架构**: API → Service → Core
- **模块化设计**: 易维护、可扩展

### 🎨 现代化UI
- 渐变色主题
- 响应式布局
- 专业的组件设计

### 📚 完整文档
- 使用指南
- 技术文档
- API文档
- 迁移指南

### 🔧 专业配置
- 集中配置管理
- 灵活的参数调整
- 环境变量支持

---

## 🎓 学习路径

### 新手（第1天）
1. ✅ 阅读本文件（你在这里！）
2. ✅ 阅读 [QUICK_START.md](QUICK_START.md)
3. ✅ 启动系统并测试
4. ✅ 上传第一个视频

### 进阶（第2-3天）
5. ✅ 阅读 [README.md](README.md)
6. ✅ 尝试所有功能
7. ✅ 理解评分标准
8. ✅ 优化拍摄技巧

### 开发者（第4-7天）
9. ✅ 阅读 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
10. ✅ 理解系统架构
11. ✅ 查看核心代码
12. ✅ 尝试定制功能

---

## 🛠️ 自定义配置

### 修改评分权重
编辑 `config/settings.py`:
```python
SCORING_CONFIG = {
    "weights": {
        "arm_score": 0.4,      # 手臂权重
        "body_score": 0.3,     # 身体权重
        "position_score": 0.2,  # 位置权重
        "stability_score": 0.1  # 稳定性权重
    }
}
```

### 修改关卡设置
编辑 `config/settings.py`:
```python
LEVEL_CONFIG = {
    "beginner": {
        "passing_score": 50,  # 初级及格分
    },
    "intermediate": {
        "passing_score": 70,  # 中级及格分
    },
    "advanced": {
        "passing_score": 85,  # 高级及格分
    }
}
```

### 修改动作模板
编辑 `data/templates/default_template.json`:
```json
{
  "arm_angle": 165,
  "arm_gap_angle": 25,
  "knee_angle": 75,
  "hip_height": 0.55,
  "arm_height": 0.45
}
```

---

## 🆘 获取帮助

### 文档资源
- 📖 [README.md](README.md) - 完整文档
- 🚀 [QUICK_START.md](QUICK_START.md) - 快速开始
- 📊 [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - 技术详解

### 技术支持
- 💬 GitHub Issues - 报告问题
- 📧 Email - 直接联系
- 📚 Wiki - 更多教程

### 常见问题
详见 [QUICK_START.md](QUICK_START.md) 的"常见问题排查"章节

---

## 📊 项目统计

- ✅ **36+** 个新建/更新文件
- ✅ **4350+** 行代码
- ✅ **1500+** 行文档
- ✅ **6** 个核心模块
- ✅ **4** 个UI组件
- ✅ **3** 层架构设计

---

## 🎯 下一步做什么？

### 立即行动
```bash
# 1. 启动系统
streamlit run app.py

# 或使用启动脚本
run.bat
```

### 然后
1. 📖 阅读 [QUICK_START.md](QUICK_START.md)
2. 🎥 上传你的第一个视频
3. 📊 查看分析结果
4. 💡 根据反馈改进动作

### 深入学习
1. 📚 阅读完整文档
2. 🔧 理解系统架构
3. ⚙️ 自定义配置
4. 🚀 添加新功能

---

## 🌟 特别提示

### ⚠️ 重要说明
- 旧版本文件仍在根目录（未删除）
- 新系统使用 `backend/` 目录下的文件
- 可以安全删除或移动旧文件到 `old_version/` 目录

### 💡 最佳实践
- 先用单帧模式快速测试
- 再用连续帧模式深度分析
- 正面拍摄，全身入镜
- 光线充足，背景简洁

### 🎮 游戏化建议
- 从初级关卡开始
- 每天练习一次
- 关注改进建议
- 追求更高分数

---

## 🎊 准备好了吗？

**现在就启动系统，开始你的排球AI训练之旅！**

```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh

# 或直接运行
streamlit run app.py
```

---

**祝你训练顺利！🏐**

---

<div align="center">

**排球AI训练系统 v3.0**

Made with ❤️ and 🤖

[📖 文档](README.md) | [🚀 快速开始](QUICK_START.md) | [📊 技术详解](PROJECT_OVERVIEW.md)

</div>

