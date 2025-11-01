"""评分卡片组件"""
import streamlit as st
import plotly.graph_objects as go


def render_score_card(score_summary):
    """
    渲染评分卡片
    
    Args:
        score_summary: 评分摘要字典
    """
    if not score_summary:
        st.warning("暂无评分数据")
        return
    
    total_score = score_summary.get("total_score", 0)
    level_info = score_summary.get("level_info", {})
    
    # 总分展示
    st.markdown("""
        <style>
        .score-container {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
            margin: 1rem 0;
        }
        .total-score {
            font-size: 4rem;
            font-weight: bold;
            margin: 0;
        }
        .score-label {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="score-container">
            <div class="total-score">{total_score}</div>
            <div class="score-label">总分 / 100</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 关卡信息
    if level_info.get("passed"):
        st.success(level_info.get("message", "恭喜通过！"))
    else:
        st.info(level_info.get("message", "继续努力！"))
    
    # 分项得分
    st.subheader("📊 分项得分")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("手臂姿态", f"{score_summary.get('arm_score', 0):.1f}/35")
        st.metric("触球位置", f"{score_summary.get('position_score', 0):.1f}/25")
    
    with col2:
        st.metric("身体重心", f"{score_summary.get('body_score', 0):.1f}/30")
        st.metric("整体稳定", f"{score_summary.get('stability_score', 0):.1f}/10")
    
    # 雷达图
    render_radar_chart(score_summary)
    
    # 反馈建议
    st.subheader("💡 改进建议")
    feedback = score_summary.get("feedback", [])
    for msg in feedback:
        st.info(msg)


def render_radar_chart(score_summary):
    """
    渲染雷达图
    
    Args:
        score_summary: 评分摘要
    """
    categories = ['手臂姿态', '身体重心', '触球位置', '整体稳定']
    values = [
        (score_summary.get('arm_score', 0) / 35) * 100,
        (score_summary.get('body_score', 0) / 30) * 100,
        (score_summary.get('position_score', 0) / 25) * 100,
        (score_summary.get('stability_score', 0) / 10) * 100,
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # 闭合图形
        theta=categories + [categories[0]],
        fill='toself',
        name='得分',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_simple_score(score_result):
    """
    渲染简单评分（无详细分析）
    
    Args:
        score_result: 评分结果字典
    """
    if not score_result:
        return
    
    total_score = score_result.get("total_score", 0)
    
    # 使用进度条显示
    st.markdown("### 总分")
    st.progress(total_score / 100)
    st.markdown(f"**{total_score} / 100**")
    
    # 显示反馈
    feedback = score_result.get("feedback", [])
    if feedback:
        st.markdown("### 反馈")
        for msg in feedback:
            st.write(f"• {msg}")

