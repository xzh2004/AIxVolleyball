"""视频上传组件"""
import streamlit as st


def render_video_uploader(key="video_uploader"):
    """
    渲染视频上传组件
    
    Args:
        key: 组件唯一标识符
        
    Returns:
        uploaded_file: 上传的文件对象
    """
    st.markdown("""
        <style>
        .upload-section {
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            background-color: #f8f9fa;
            margin: 1rem 0;
        }
        .upload-title {
            font-size: 1.3rem;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .upload-hint {
            color: #666;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
            <div class="upload-section">
                <div class="upload-title">📹 上传你的垫球视频</div>
                <div class="upload-hint">支持 MP4, AVI, MOV, MKV 格式，文件大小不超过 50MB</div>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "选择视频文件",
            type=['mp4', 'avi', 'mov', 'mkv'],
            key=key,
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.success(f"✅ 已上传: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.2f} MB)")
        
        return uploaded_file


def render_analysis_mode_selector():
    """
    渲染分析模式选择器
    
    Returns:
        str: 选择的分析模式
    """
    st.markdown("### ⚙️ 分析模式")
    
    mode = st.radio(
        "选择分析模式",
        options=["single", "sequence"],
        format_func=lambda x: "🎯 单帧分析（快速）" if x == "single" else "🎬 连续帧分析（详细）",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if mode == "single":
        st.info("💡 单帧模式：提取关键帧进行快速分析，适合初学者")
    else:
        st.info("💡 连续帧模式：分析完整动作序列，提供流畅度、完整性等深度评估")
    
    return mode


def render_visualization_selector():
    """
    渲染可视化类型选择器
    
    Returns:
        str: 选择的可视化类型
    """
    st.markdown("### 🎨 可视化类型")
    
    vis_type = st.selectbox(
        "选择可视化类型",
        options=["overlay", "skeleton", "comparison", "trajectory"],
        format_func=lambda x: {
            "overlay": "🎥 骨架叠加（推荐）",
            "skeleton": "🦴 纯骨架动画",
            "comparison": "📊 左右对比",
            "trajectory": "📈 轨迹追踪"
        }[x],
        label_visibility="collapsed"
    )
    
    descriptions = {
        "overlay": "在原视频上叠加姿态骨架，最直观",
        "skeleton": "白色背景上的抽象骨架，最清晰",
        "comparison": "原视频与骨架并排对比，最专业",
        "trajectory": "实时绘制关键点运动路径，最动感"
    }
    
    st.caption(descriptions[vis_type])
    
    return vis_type

