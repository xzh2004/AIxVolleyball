"""
排球AI闯关训练系统 - Streamlit主界面
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

from pose_detector import PoseDetector
from scorer import VolleyballScorer
from video_processor import VideoProcessor
from sequence_analyzer import SequenceAnalyzer
from trajectory_visualizer import TrajectoryVisualizer


# 页面配置
st.set_page_config(
    page_title="🏐 排球AI闯关训练",
    page_icon="🏐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .big-font {
        font-size: 50px !important;
        font-weight: bold;
        text-align: center;
    }
    .score-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .feedback-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'total_score' not in st.session_state:
        st.session_state.total_score = 0
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0


def main():
    init_session_state()
    
    # 标题
    st.markdown("<h1 style='text-align: center;'>🏐 排球AI闯关训练系统</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>AI驱动的排球动作识别与评分系统 - Demo版</p>", unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("📊 训练统计")
        st.metric("当前关卡", f"第 {st.session_state.level} 关")
        st.metric("累计得分", st.session_state.total_score)
        st.metric("练习次数", st.session_state.attempts)
        
        st.markdown("---")
        st.header("🎯 关卡说明")
        
        levels = {
            1: {"name": "垫球入门", "desc": "掌握基本垫球姿势", "pass_score": 60},
            2: {"name": "标准垫球", "desc": "达到标准垫球动作", "pass_score": 75},
            3: {"name": "高级垫球", "desc": "追求完美垫球技巧", "pass_score": 85},
        }
        
        current_level = levels.get(st.session_state.level, levels[1])
        st.info(f"**{current_level['name']}**\n\n{current_level['desc']}\n\n通关分数: {current_level['pass_score']}")
        
        st.markdown("---")
        st.header("📖 评分标准")
        st.write("""
        - 🤲 **手臂姿态** (40分)
          - 双臂伸直
          - 间距适中
        
        - 🧘 **身体重心** (30分)
          - 膝盖弯曲
          - 重心下沉
        
        - 📍 **触球位置** (20分)
          - 腰腹前方
          - 高度适中
        
        - ⚖️ **整体稳定** (10分)
          - 姿态清晰
          - 识别准确
        """)
        
        if st.button("🔄 重置进度"):
            st.session_state.level = 1
            st.session_state.total_score = 0
            st.session_state.attempts = 0
            st.rerun()
    
    # 主界面
    tab1, tab2, tab3 = st.tabs(["🎥 视频上传", "📸 使用说明", "🏆 关于项目"])
    
    with tab1:
        st.header("上传你的垫球视频")
        
        # 文件上传
        uploaded_file = st.file_uploader(
            "选择视频文件 (MP4, AVI)",
            type=['mp4', 'avi', 'mov'],
            help="建议: 正面拍摄，全身入镜，光线充足，时长3-10秒"
        )
        
        if uploaded_file is not None:
            # 显示视频信息
            st.success(f"✅ 已上传: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.2f} MB)")
            
            # 处理选项
            col1, col2, col3 = st.columns(3)
            with col1:
                analysis_mode = st.selectbox(
                    "分析模式",
                    ['single', 'sequence'],
                    format_func=lambda x: '🎯 单帧分析（快速）' if x == 'single' else '🎬 连续帧分析（推荐）'
                )
            
            with col2:
                if analysis_mode == 'single':
                    frame_method = st.selectbox(
                        "关键帧提取方法",
                        ['middle', 'motion'],
                        format_func=lambda x: '中间帧' if x == 'middle' else '运动峰值帧'
                    )
                else:
                    frame_method = 'all'
                    st.selectbox(
                        "采样频率",
                        ['每秒2帧（推荐）'],
                        disabled=True
                    )
            
            with col3:
                st.write("")
                st.write("")
                process_button = st.button("🚀 开始分析", type="primary", use_container_width=True)
            
            # 模式说明
            if analysis_mode == 'single':
                st.info("💡 单帧模式：快速分析单个关键帧，适合快速测试")
            else:
                st.success("💡 连续帧模式：分析整个动作过程，评估流畅度、完整性和轨迹，更准确！")
            
            if process_button:
                if analysis_mode == 'single':
                    process_video(uploaded_file, frame_method)
                else:
                    process_video_sequence(uploaded_file)
    
    with tab2:
        st.header("📸 拍摄指南")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ 正确示例")
            st.success("""
            1. **正面拍摄**：摄像头与人正面相对
            2. **全身入镜**：头到脚完整可见
            3. **光线充足**：避免逆光和阴影
            4. **背景简洁**：纯色背景最佳
            5. **动作清晰**：保持3-10秒的动作展示
            6. **稳定拍摄**：固定手机或使用支架
            """)
        
        with col2:
            st.subheader("❌ 常见错误")
            st.error("""
            1. **侧面角度**：无法准确识别姿态
            2. **身体遮挡**：手臂或腿部被遮挡
            3. **光线不足**：图像模糊不清
            4. **距离太近**：身体部分超出画面
            5. **背景复杂**：干扰识别准确度
            6. **视频抖动**：影响关键帧提取
            """)
        
        st.markdown("---")
        st.subheader("🎬 推荐设置")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("视频时长", "3-10秒", help="过短可能无法捕捉动作，过长影响处理速度")
        with col2:
            st.metric("拍摄距离", "2-3米", help="确保全身入镜且不会太远")
        with col3:
            st.metric("分辨率", "720P+", help="高清视频识别更准确")
    
    with tab3:
        st.header("🏆 关于项目")
        
        st.markdown("""
        ### 🎯 项目简介
        
        这是一个基于AI的排球动作识别与评分系统，通过计算机视觉技术分析垫球动作的标准度，
        并以游戏化的方式帮助用户提升技能。
        
        ### 🔧 技术栈
        
        - **姿态识别**: MediaPipe Pose
        - **视频处理**: OpenCV
        - **前端界面**: Streamlit
        - **数值计算**: NumPy, SciPy
        
        ### 📈 功能特点
        
        - ✅ 实时姿态关键点检测
        - ✅ 多维度动作评分算法
        - ✅ 智能反馈与改进建议
        - ✅ 游戏化关卡系统
        - ✅ 可视化骨架叠加显示
        
        ### 🚀 未来规划
        
        - [ ] 支持更多动作类型（扣球、发球）
        - [ ] 实时摄像头识别
        - [ ] 动作历史记录与分析
        - [ ] 社交功能与排行榜
        - [ ] 移动端App
        
        ### 👨‍💻 开发信息
        
        - **版本**: v1.0.0 Demo
        - **更新日期**: 2025-10-28
        - **开源协议**: MIT
        
        ---
        
        Made with ❤️ for volleyball lovers
        """)


def process_video(uploaded_file, frame_method):
    """处理上传的视频"""
    
    # 进度条
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 初始化组件
        status_text.text("⏳ 正在初始化...")
        progress_bar.progress(10)
        
        processor = VideoProcessor()
        detector = PoseDetector()
        scorer = VolleyballScorer()
        
        # 保存上传文件
        status_text.text("⏳ 正在保存视频...")
        progress_bar.progress(20)
        temp_path = processor.save_uploaded_file(uploaded_file)
        
        # 获取视频信息
        video_info = processor.get_video_info(temp_path)
        if video_info:
            st.info(f"📹 视频信息: {video_info['width']}x{video_info['height']}, "
                   f"{video_info['fps']:.1f}fps, {video_info['duration']}秒")
        
        # 提取关键帧
        status_text.text("⏳ 正在提取关键帧...")
        progress_bar.progress(40)
        key_frame = processor.extract_key_frame(temp_path, method=frame_method)
        
        # 姿态识别
        status_text.text("⏳ 正在识别姿态...")
        progress_bar.progress(60)
        landmarks, annotated_image = detector.detect_pose(key_frame)
        
        # 评分
        status_text.text("⏳ 正在计算得分...")
        progress_bar.progress(80)
        score_result = scorer.score_pose(landmarks)
        
        progress_bar.progress(100)
        status_text.text("✅ 分析完成！")
        time.sleep(0.5)
        
        # 清除进度条
        progress_bar.empty()
        status_text.empty()
        
        # 显示结果
        display_results(key_frame, annotated_image, score_result, scorer)
        
        # 更新统计
        st.session_state.attempts += 1
        st.session_state.total_score += score_result['total_score']
        
        # 检查是否通关
        check_level_up(score_result['total_score'])
        
    except Exception as e:
        status_text.empty()
        progress_bar.empty()
        st.error(f"❌ 处理失败: {str(e)}")
        st.exception(e)


def display_results(original_frame, annotated_frame, score_result, scorer):
    """显示分析结果"""
    
    st.markdown("---")
    st.header("📊 分析结果")
    
    # 得分展示
    total_score = score_result['total_score']
    grade, grade_msg = scorer.get_grade(total_score)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="score-box">
            <h1 style='font-size: 60px; margin: 0;'>{total_score}</h1>
            <h3 style='margin: 5px 0;'>总分 / 100</h3>
            <h2 style='margin: 10px 0;'>等级: {grade}</h2>
            <p style='font-size: 18px;'>{grade_msg}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 详细得分
    st.subheader("📈 详细评分")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🤲 手臂姿态",
            f"{score_result['arm_score']:.1f} / 40",
            delta=f"{score_result['arm_score']/40*100:.0f}%"
        )
    
    with col2:
        st.metric(
            "🧘 身体重心",
            f"{score_result['body_score']:.1f} / 30",
            delta=f"{score_result['body_score']/30*100:.0f}%"
        )
    
    with col3:
        st.metric(
            "📍 触球位置",
            f"{score_result['position_score']:.1f} / 20",
            delta=f"{score_result['position_score']/20*100:.0f}%"
        )
    
    with col4:
        st.metric(
            "⚖️ 整体稳定",
            f"{score_result['stability_score']:.1f} / 10",
            delta=f"{score_result['stability_score']/10*100:.0f}%"
        )
    
    # 图像对比
    st.subheader("🖼️ 姿态识别结果")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(
            cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB),
            caption="原始画面",
            use_column_width=True
        )
    
    with col2:
        st.image(
            cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB),
            caption="姿态识别（骨架叠加）",
            use_column_width=True
        )
    
    # 反馈建议
    st.subheader("💡 改进建议")
    
    feedback_html = "<div class='feedback-box'>"
    for feedback in score_result['feedback']:
        if '✅' in feedback:
            feedback_html += f"<p style='color: green; margin: 8px 0;'>{feedback}</p>"
        elif '❌' in feedback:
            feedback_html += f"<p style='color: red; margin: 8px 0;'>{feedback}</p>"
        else:
            feedback_html += f"<p style='color: orange; margin: 8px 0;'>{feedback}</p>"
    feedback_html += "</div>"
    
    st.markdown(feedback_html, unsafe_allow_html=True)


def process_video_sequence(uploaded_file):
    """处理视频序列（连续帧分析）"""
    
    # 进度条
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 初始化组件
        status_text.text("⏳ 正在初始化...")
        progress_bar.progress(10)
        
        processor = VideoProcessor()
        analyzer = SequenceAnalyzer()
        scorer = VolleyballScorer()
        visualizer = TrajectoryVisualizer()
        
        # 保存上传文件
        status_text.text("⏳ 正在保存视频...")
        progress_bar.progress(20)
        temp_path = processor.save_uploaded_file(uploaded_file)
        
        # 获取视频信息
        video_info = processor.get_video_info(temp_path)
        if video_info:
            st.info(f"📹 视频信息: {video_info['width']}x{video_info['height']}, "
                   f"{video_info['fps']:.1f}fps, {video_info['duration']}秒")
        
        # 提取连续帧
        status_text.text("⏳ 正在提取视频帧...")
        progress_bar.progress(30)
        frames = processor.extract_key_frame(temp_path, method='all')
        st.info(f"📊 提取了 {len(frames)} 帧进行分析")
        
        # 序列分析
        status_text.text(f"⏳ 正在分析 {len(frames)} 帧姿态...")
        progress_bar.progress(50)
        sequence_result = analyzer.analyze_sequence(frames)
        
        # 获取最佳帧进行详细评分
        status_text.text("⏳ 正在计算综合得分...")
        progress_bar.progress(70)
        best_idx = sequence_result['best_frame_idx']
        best_landmarks = sequence_result['frames_data'][best_idx]['landmarks']
        pose_score = scorer.score_pose(best_landmarks)
        
        # 获取序列摘要
        status_text.text("⏳ 正在生成分析报告...")
        progress_bar.progress(90)
        sequence_summary = analyzer.get_sequence_summary(sequence_result)
        
        progress_bar.progress(100)
        status_text.text("✅ 分析完成！")
        time.sleep(0.5)
        
        # 清除进度条
        progress_bar.empty()
        status_text.empty()
        
        # 显示结果
        display_sequence_results(
            frames,
            sequence_result,
            pose_score,
            sequence_summary,
            scorer,
            visualizer
        )
        
        # 更新统计（使用综合得分）
        combined_score = int(pose_score['total_score'] * 0.6 + sequence_summary['sequence_score'] * 0.4)
        st.session_state.attempts += 1
        st.session_state.total_score += combined_score
        
        # 检查是否通关
        check_level_up(combined_score)
        
    except Exception as e:
        status_text.empty()
        progress_bar.empty()
        st.error(f"❌ 处理失败: {str(e)}")
        st.exception(e)


def display_sequence_results(frames, sequence_result, pose_score, sequence_summary, scorer, visualizer):
    """显示序列分析结果"""
    
    st.markdown("---")
    st.header("📊 连续帧分析结果")
    
    # 综合得分展示
    best_idx = sequence_result['best_frame_idx']
    pose_total = pose_score['total_score']
    sequence_total = sequence_summary['sequence_score']
    combined_score = int(pose_total * 0.6 + sequence_total * 0.4)
    
    grade, grade_msg = scorer.get_grade(combined_score)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="score-box">
            <h1 style='font-size: 60px; margin: 0;'>{combined_score}</h1>
            <h3 style='margin: 5px 0;'>综合得分 / 100</h3>
            <h2 style='margin: 10px 0;'>等级: {grade}</h2>
            <p style='font-size: 18px;'>{grade_msg}</p>
            <p style='font-size: 14px; opacity: 0.8;'>姿态分: {pose_total} | 动作分: {int(sequence_total)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 详细评分（两个维度）
    st.subheader("📈 双维度评分")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 姿态质量 (60%)")
        subcol1, subcol2, subcol3, subcol4 = st.columns(4)
        with subcol1:
            st.metric("手臂", f"{pose_score['arm_score']:.0f}/40")
        with subcol2:
            st.metric("重心", f"{pose_score['body_score']:.0f}/30")
        with subcol3:
            st.metric("位置", f"{pose_score['position_score']:.0f}/20")
        with subcol4:
            st.metric("稳定", f"{pose_score['stability_score']:.0f}/10")
    
    with col2:
        st.markdown("#### 🎬 动作质量 (40%)")
        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol1:
            st.metric("流畅度", f"{sequence_summary['smoothness_score']:.0f}/100")
        with subcol2:
            st.metric("完整性", f"{sequence_summary['completeness_score']:.0f}/100")
        with subcol3:
            st.metric("一致性", f"{sequence_summary['consistency_score']:.0f}/100")
    
    # 帧统计
    st.info(f"📊 分析了 {sequence_summary['total_frames']} 帧，"
           f"{sequence_summary['valid_frames']} 帧有效，"
           f"第 {best_idx + 1} 帧姿态最佳")
    
    # 图像对比（最佳帧）
    st.subheader("🖼️ 最佳姿态展示")
    
    best_frame = frames[best_idx]
    best_annotated = sequence_result['annotated_frames'][best_idx]
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(
            cv2.cvtColor(best_frame, cv2.COLOR_BGR2RGB),
            caption=f"原始画面（第 {best_idx + 1} 帧）",
            use_column_width=True
        )
    with col2:
        st.image(
            cv2.cvtColor(best_annotated, cv2.COLOR_BGR2RGB),
            caption="姿态识别（骨架叠加）",
            use_column_width=True
        )
    
    # 轨迹可视化
    st.subheader("🎯 动作轨迹分析")
    
    try:
        # 创建轨迹图
        trajectory_plot = visualizer.create_trajectory_plot(
            sequence_result['trajectories'],
            frames[0].shape[1],
            frames[0].shape[0]
        )
        st.image(trajectory_plot, caption="关键点运动轨迹", use_column_width=True)
    except Exception as e:
        st.warning(f"轨迹可视化失败: {str(e)}")
    
    # 角度时间轴
    st.subheader("📈 角度变化分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            all_landmarks = [f['landmarks'] for f in sequence_result['frames_data']]
            arm_timeline = visualizer.create_angle_timeline(all_landmarks, 'arm')
            st.image(arm_timeline, caption="手臂角度时间轴", use_column_width=True)
        except Exception as e:
            st.warning(f"手臂角度分析失败: {str(e)}")
    
    with col2:
        try:
            knee_timeline = visualizer.create_angle_timeline(all_landmarks, 'knee')
            st.image(knee_timeline, caption="膝盖角度时间轴", use_column_width=True)
        except Exception as e:
            st.warning(f"膝盖角度分析失败: {str(e)}")
    
    # 综合反馈
    st.subheader("💡 综合改进建议")
    
    all_feedback = []
    all_feedback.extend(sequence_summary['feedback'])
    all_feedback.extend(pose_score['feedback'])
    
    feedback_html = "<div class='feedback-box'>"
    for feedback in all_feedback:
        if '✅' in feedback:
            feedback_html += f"<p style='color: green; margin: 8px 0;'>{feedback}</p>"
        elif '❌' in feedback:
            feedback_html += f"<p style='color: red; margin: 8px 0;'>{feedback}</p>"
        else:
            feedback_html += f"<p style='color: orange; margin: 8px 0;'>{feedback}</p>"
    feedback_html += "</div>"
    
    st.markdown(feedback_html, unsafe_allow_html=True)


def check_level_up(score):
    """检查是否可以升级"""
    levels = {
        1: 60,
        2: 75,
        3: 85,
    }
    
    current_level = st.session_state.level
    pass_score = levels.get(current_level, 100)
    
    if score >= pass_score and current_level < max(levels.keys()):
        st.balloons()
        st.success(f"🎉 恭喜通关！解锁第 {current_level + 1} 关！")
        
        if st.button("⬆️ 进入下一关", type="primary"):
            st.session_state.level += 1
            st.rerun()
    elif score >= pass_score and current_level == max(levels.keys()):
        st.balloons()
        st.success("🏆 恭喜你完成所有关卡！你已经是排球大师了！")
    else:
        remaining = pass_score - score
        st.info(f"💪 再得 {remaining} 分即可通关！继续加油！")


if __name__ == "__main__":
    main()

