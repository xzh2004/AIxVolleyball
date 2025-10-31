"""
用户信息组件
显示用户昵称、头像、等级、积分（假数据）
"""
import streamlit as st

def render_user_info():
    """渲染用户信息栏"""
    # 假数据
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'nickname': '排球小将',
            'avatar': '🏐',
            'level': 15,
            'points': 2850
        }
    
    user = st.session_state.user_data
    
    # 创建顶部信息栏
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown(f"### {user['avatar']}")
    
    with col2:
        st.markdown(f"""
        **{user['nickname']}**  
        🌟 等级 {user['level']} | 💎 积分 {user['points']}
        """)
    
    with col3:
        if st.button("📊 我的数据", use_container_width=True):
            st.info("个人数据功能开发中...")
    
    st.divider()

