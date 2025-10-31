"""页面头部组件"""
import streamlit as st


def render_header():
    """渲染页面头部"""
    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        .main-header p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="main-header">
            <h1>🏐 排球AI训练系统</h1>
            <p>AI-Powered Volleyball Training System</p>
        </div>
    """, unsafe_allow_html=True)


def render_level_badge(level_info):
    """
    渲染关卡徽章
    
    Args:
        level_info: 关卡信息字典
    """
    level_colors = {
        "beginner": "#4CAF50",
        "intermediate": "#FF9800",
        "advanced": "#F44336"
    }
    
    level_icons = {
        "beginner": "🌱",
        "intermediate": "🌟",
        "advanced": "🏆"
    }
    
    level = level_info.get("level", "beginner")
    level_name = level_info.get("level_name", "初级")
    color = level_colors.get(level, "#4CAF50")
    icon = level_icons.get(level, "🌱")
    
    st.markdown(f"""
        <style>
        .level-badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: {color};
            color: white;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1rem;
            margin: 0.5rem 0;
        }}
        </style>
        <div class="level-badge">
            {icon} {level_name}关卡
        </div>
    """, unsafe_allow_html=True)

