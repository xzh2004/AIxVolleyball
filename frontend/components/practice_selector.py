"""
练习选择组件
显示当前位置的练习项目，只有垫球可选
"""
import streamlit as st

def render_practice_selector():
    """渲染练习选择页面"""
    position = st.session_state.get('selected_position', 'libero')
    
    # 返回按钮
    if st.button("← 返回位置选择", key="back_to_position"):
        st.session_state.page = 'position_selection'
        st.rerun()
    
    st.title("🏐 选择练习项目")
    st.markdown("---")
    
    # 自由人的练习项目
    practices = {
        'passing': {
            'name': '垫球练习',
            'icon': '🤲',
            'description': 'AI智能分析你的垫球动作，提供专业评分和建议',
            'level': '初级-高级',
            'enabled': True
        },
        'serve': {
            'name': '发球练习',
            'icon': '🎯',
            'description': '提升发球的准确性和力量',
            'level': '中级-高级',
            'enabled': False
        },
        'spike': {
            'name': '扣球练习',
            'icon': '⚡',
            'description': '掌握扣球技巧，提升进攻能力',
            'level': '中级-高级',
            'enabled': False
        },
        'block': {
            'name': '拦网练习',
            'icon': '🧱',
            'description': '提升拦网时机和手型',
            'level': '中级-高级',
            'enabled': False
        },
        'set': {
            'name': '二传练习',
            'icon': '🎪',
            'description': '练习传球的精准度和节奏',
            'level': '中级-高级',
            'enabled': False
        },
        'defense': {
            'name': '防守练习',
            'icon': '🛡️',
            'description': '提升防守反应和移动能力',
            'level': '初级-高级',
            'enabled': False
        }
    }
    
    st.markdown("### 🛡️ 自由人训练项目")
    st.markdown("")
    
    # 使用2列布局
    col1, col2 = st.columns(2)
    
    keys = list(practices.keys())
    for i, key in enumerate(keys):
        practice = practices[key]
        
        with col1 if i % 2 == 0 else col2:
            with st.container():
                if practice['enabled']:
                    st.markdown(f"### {practice['icon']} {practice['name']}")
                    st.markdown(f"**{practice['description']}**")
                    st.markdown(f"📊 难度：{practice['level']}")
                    
                    if st.button(
                        "开始练习 →", 
                        key=f"practice_{key}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.selected_practice = key
                        st.session_state.page = 'training'
                        st.rerun()
                else:
                    st.markdown(f"### {practice['icon']} {practice['name']} 🔒")
                    st.markdown(f"{practice['description']}")
                    st.markdown(f"📊 难度：{practice['level']}")
                    st.button(
                        "🔒 敬请期待", 
                        key=f"practice_{key}",
                        use_container_width=True,
                        disabled=True
                    )
                
                st.markdown("---")
    
    st.info("💡 提示：目前开放了垫球练习，更多练习项目正在开发中！")

