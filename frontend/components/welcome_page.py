"""
欢迎/引导页面组件
"""
import streamlit as st
import time

def render_welcome_page():
    """渲染欢迎页面（首次进入时）"""
    
    # 页面容器
    st.markdown("""
        <style>
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 70vh;
            text-align: center;
            animation: fadeIn 1s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .welcome-title {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            animation: slideDown 0.8s ease-out;
        }
        
        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .welcome-subtitle {
            font-size: 1.5rem;
            color: #666;
            margin-bottom: 3rem;
            animation: slideUp 0.8s ease-out 0.2s backwards;
        }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .feature-card {
            background: linear-gradient(145deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            animation: scaleIn 0.6s ease-out backwards;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }
        
        @keyframes scaleIn {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .feature-desc {
            color: #666;
            font-size: 0.95rem;
        }
        
        .start-button {
            font-size: 1.2rem;
            padding: 1rem 3rem;
            border-radius: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            animation: pulse 2s ease-in-out infinite;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .start-button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .loading-dots {
            display: inline-block;
            animation: dots 1.5s steps(4, end) infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60%, 100% { content: '...'; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 主容器
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    
    # 标题和副标题
    st.markdown('<h1 class="welcome-title">🏐 排球AI训练系统</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-subtitle">让科技助力你的排球训练之路</p>', unsafe_allow_html=True)
    
    # 特色功能展示
    cols = st.columns(3)
    
    features = [
        {
            "icon": "🎯",
            "title": "精准识别",
            "desc": "基于AI的动作识别技术，实时分析你的排球动作"
        },
        {
            "icon": "📊",
            "title": "数据分析",
            "desc": "全方位的数据统计，帮助你了解训练进度"
        },
        {
            "icon": "📚",
            "title": "战术学习",
            "desc": "丰富的战术题库，提升你的排球战术素养"
        }
    ]
    
    for col, feature in zip(cols, features):
        with col:
            st.markdown(f"""
                <div class="feature-card" style="animation-delay: {0.3 + cols.index(col) * 0.1}s;">
                    <div class="feature-icon">{feature['icon']}</div>
                    <div class="feature-title">{feature['title']}</div>
                    <div class="feature-desc">{feature['desc']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 开始按钮
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 开始训练", key="start_training", use_container_width=True):
            st.session_state.welcomed = True
            st.session_state.page = 'position_selection'  # 跳转到位置选择页面
            st.rerun()
    
    # 底部信息
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; color: #999; font-size: 0.85rem;">
            <p>💡 提示：选择你的位置，开始专属训练</p>
            <p style="margin-top: 0.5rem;">Version 2.0 | Powered by AI</p>
        </div>
    """, unsafe_allow_html=True)


def render_loading_page(message="加载中", duration=1.5):
    """渲染加载页面
    
    Args:
        message: 加载提示信息
        duration: 加载持续时间（秒）
    """
    st.markdown("""
        <style>
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 70vh;
            text-align: center;
        }
        
        .spinner {
            width: 60px;
            height: 60px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 2rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            font-size: 1.5rem;
            color: #666;
            font-weight: 600;
        }
        
        .progress-bar {
            width: 300px;
            height: 6px;
            background: #f3f3f3;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 1rem;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 10px;
            animation: progress 1.5s ease-in-out forwards;
        }
        
        @keyframes progress {
            from { width: 0%; }
            to { width: 100%; }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="loading-container">
            <div class="spinner"></div>
            <div class="loading-text">{message}...</div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    time.sleep(duration)

