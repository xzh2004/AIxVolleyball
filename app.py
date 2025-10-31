"""
排球AI训练系统 - 多页面主应用
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import cv2
import os

# 导入后端API
from backend.api import VolleyballAPI

# 导入前端组件
from frontend.components.user_info import render_user_info
from frontend.components.position_selector import render_position_selector
from frontend.components.practice_selector import render_practice_selector
from frontend.components.header import render_header, render_level_badge
from frontend.components.score_card import render_score_card
from frontend.components.video_uploader import (
    render_video_uploader,
    render_analysis_mode_selector,
    render_visualization_selector
)

# 导入配置
from config.settings import STREAMLIT_CONFIG

# 页面配置
st.set_page_config(
    page_title="排球AI训练系统",
    page_icon="🏐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem 2rem;
    }
    .stButton>button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """主函数"""
    
    # 初始化session state
    if 'page' not in st.session_state:
        st.session_state.page = 'position_selection'
    
    if 'api' not in st.session_state:
        st.session_state.api = VolleyballAPI()
    
    # 渲染用户信息栏（所有页面都显示）
    render_user_info()
    
    # 根据当前页面渲染不同内容
    if st.session_state.page == 'position_selection':
        render_position_selector()
    
    elif st.session_state.page == 'practice_selection':
        render_practice_selector()
    
    elif st.session_state.page == 'training':
        render_training_page()


def render_training_page():
    """渲染训练页面（垫球练习）"""
    api = st.session_state.api
    
    # 返回按钮
    if st.button("← 返回练习选择", key="back_to_practice"):
        st.session_state.page = 'practice_selection'
        st.rerun()
    
    st.title("🤲 垫球训练")
    st.markdown("---")
    
    # 使用tabs组织功能
    tab1, tab2 = st.tabs(["🎯 动作分析", "🎥 视频可视化"])
    
    with tab1:
        render_analysis_tab(api)
    
    with tab2:
        render_visualization_tab(api)


def render_analysis_tab(api):
    """渲染动作分析标签页"""
    st.markdown("### 📤 上传你的垫球视频")
    
    # 上传视频
    uploaded_file = render_video_uploader("analysis_uploader")
    
    if uploaded_file:
        # 验证文件
        is_valid, error_msg = api.validate_video_file(uploaded_file)
        if not is_valid:
            st.error(error_msg)
            return
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📹 原始视频")
            st.video(uploaded_file)
        
        with col2:
            st.markdown("#### ⚙️ 分析设置")
            
            # 选择分析模式
            analysis_mode = render_analysis_mode_selector()
            
            st.markdown("")
            
            # 分析按钮
            if st.button("🚀 开始AI分析", key="analyze_btn", use_container_width=True, type="primary"):
                with st.spinner("🔍 AI正在分析中，请稍候..."):
                    # 调用API分析
                    result = api.analyze_uploaded_video(
                        uploaded_file,
                        analysis_mode=analysis_mode
                    )
                    
                    # 保存结果到session state
                    st.session_state.analysis_result = result
                    st.rerun()
        
        st.markdown("---")
        
        # 显示分析结果
        if 'analysis_result' in st.session_state:
            result = st.session_state.analysis_result
            
            if result.get("success"):
                st.success("✅ 分析完成！")
                
                # 显示分析模式
                mode_name = "单帧快速分析" if result.get("analysis_mode") == "single_frame" else "连续帧深度分析"
                st.info(f"📊 分析模式: {mode_name}")
                
                # 显示评分结果
                score_result = result.get("score")
                if score_result:
                    # 获取评分摘要
                    score_summary = api.get_score_summary(score_result)
                    
                    # 渲染评分卡片
                    render_score_card(score_summary)
                    
                    col1, col2 = st.columns(2)
                    
                    # 显示姿态图像
                    with col1:
                        if result.get("pose_image") is not None:
                            st.markdown("### 🎨 姿态检测结果")
                            pose_img_rgb = cv2.cvtColor(result["pose_image"], cv2.COLOR_BGR2RGB)
                            st.image(pose_img_rgb, caption="姿态关键点标注", use_container_width=True)
                    
                    # 如果是序列分析，显示额外信息
                    with col2:
                        if result.get("analysis_mode") == "sequence":
                            if result.get("trajectory_plot"):
                                st.markdown("### 📈 运动轨迹分析")
                                st.image(result["trajectory_plot"], use_container_width=True)
                    
                    if result.get("sequence_scores"):
                        st.markdown("### 📊 序列评分详情")
                        seq_scores = result["sequence_scores"]
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("流畅度", f"{seq_scores.get('smoothness', 0):.1f}/100", 
                                     help="动作的连贯性和平滑程度")
                        with col2:
                            st.metric("完整性", f"{seq_scores.get('completeness', 0):.1f}/100",
                                     help="动作的完整程度")
                        with col3:
                            st.metric("一致性", f"{seq_scores.get('consistency', 0):.1f}/100",
                                     help="各帧动作的一致性")
                
                else:
                    st.warning("未能获取评分结果")
            else:
                error_msg = result.get("error", "未知错误")
                st.error(f"❌ 分析失败: {error_msg}")


def render_visualization_tab(api):
    """渲染视频可视化标签页"""
    st.markdown("### 🎬 生成可视化视频")
    st.info("💡 将你的动作转换为专业的训练分析视频")
    
    # 上传视频
    uploaded_file = render_video_uploader("vis_uploader")
    
    if uploaded_file:
        # 验证文件
        is_valid, error_msg = api.validate_video_file(uploaded_file)
        if not is_valid:
            st.error(error_msg)
            return
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📹 原始视频")
            st.video(uploaded_file)
            
            st.markdown("#### 🎨 可视化类型")
            vis_type = render_visualization_selector()
            
            st.markdown("")
            
            # 生成按钮
            if st.button("🎬 生成可视化视频", key="generate_btn", use_container_width=True, type="primary"):
                with st.spinner("🎨 正在生成可视化视频，请稍候..."):
                    success, output_path, error = api.generate_visualization(
                        uploaded_file,
                        vis_type=vis_type
                    )
                    
                    if success:
                        st.session_state.generated_video = output_path
                        st.rerun()
                    else:
                        st.error(f"❌ 生成失败: {error}")
        
        with col2:
            # 显示生成的视频
            if 'generated_video' in st.session_state:
                output_path = st.session_state.generated_video
                
                st.markdown("#### ✅ 生成结果")
                if os.path.exists(output_path):
                    st.video(output_path)
                    
                    # 下载按钮
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="⬇️ 下载视频",
                            data=f,
                            file_name=os.path.basename(output_path),
                            mime="video/mp4",
                            use_container_width=True
                        )


if __name__ == "__main__":
    main()
