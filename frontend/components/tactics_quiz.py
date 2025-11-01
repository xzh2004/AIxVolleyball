"""
战术学习题库组件
"""
import streamlit as st
import json
import random
from pathlib import Path

def load_questions():
    """加载题库"""
    questions_file = Path("data/tactics_questions.json")
    if questions_file.exists():
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data["questions"], data["categories"], data["difficulty_levels"]
    return [], [], []

def render_tactics_quiz():
    """渲染战术学习题库页面"""
    
    # 加载题库
    questions, categories, difficulty_levels = load_questions()
    
    if not questions:
        st.error("题库加载失败！")
        return
    
    # 初始化 session state
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question_idx" not in st.session_state:
        st.session_state.current_question_idx = 0
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False
    if "show_explanation" not in st.session_state:
        st.session_state.show_explanation = False
    
    # 自定义CSS - 始终加载
    load_quiz_styles()
    
    # 如果还没开始测验，显示配置界面
    if not st.session_state.quiz_started:
        render_quiz_config(questions, categories, difficulty_levels)
    elif st.session_state.quiz_finished:
        render_quiz_results()
    else:
        render_quiz_question()


def load_quiz_styles():
    """加载题库页面的CSS样式"""
    st.markdown("""
        <style>
        .quiz-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
        }
        
        .quiz-header {
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .quiz-stats {
            display: flex;
            justify-content: space-around;
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .question-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .question-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .question-number {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .question-category {
            background: #e9ecef;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: #666;
            font-size: 0.9rem;
        }
        
        .question-difficulty {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }
        
        .difficulty-simple {
            background: #d4edda;
            color: #155724;
        }
        
        .difficulty-medium {
            background: #fff3cd;
            color: #856404;
        }
        
        .difficulty-hard {
            background: #f8d7da;
            color: #721c24;
        }
        
        .question-text {
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
            margin: 1.5rem 0;
            line-height: 1.6;
        }
        
        .option-button {
            width: 100%;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            background: white;
            text-align: left;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1rem;
        }
        
        .option-button:hover {
            border-color: #667eea;
            background: #f8f9fa;
            transform: translateX(5px);
        }
        
        .option-correct {
            border-color: #28a745;
            background: #d4edda;
        }
        
        .option-wrong {
            border-color: #dc3545;
            background: #f8d7da;
        }
        
        .explanation-box {
            background: #e7f3ff;
            border-left: 4px solid #667eea;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1.5rem;
        }
        
        .explanation-title {
            font-weight: 700;
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        .progress-bar-custom {
            height: 10px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .progress-fill-custom {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.5s ease;
        }
        
        .result-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem;
            border-radius: 15px;
            color: white;
            text-align: center;
        }
        
        .result-score {
            font-size: 4rem;
            font-weight: 700;
            margin: 1rem 0;
        }
        
        .result-message {
            font-size: 1.5rem;
            margin: 1rem 0;
        }
        
        .result-details {
            display: flex;
            justify-content: space-around;
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)


def render_quiz_config(questions, categories, difficulty_levels):
    """渲染测验配置界面"""
    
    st.markdown("""
        <div class="quiz-container">
            <div class="quiz-header">📚 战术学习题库</div>
            <p style="text-align: center; font-size: 1.1rem; opacity: 0.9;">
                通过智能答题提升你的排球战术素养
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ 测验设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 选择分类
        selected_categories = st.multiselect(
            "选择题目类别",
            categories,
            default=categories[:3],
            help="可以选择多个类别"
        )
    
    with col2:
        # 选择难度
        selected_difficulty = st.multiselect(
            "选择难度",
            difficulty_levels,
            default=difficulty_levels,
            help="可以选择多个难度"
        )
    
    # 选择题目数量
    num_questions = st.slider(
        "题目数量",
        min_value=5,
        max_value=30,
        value=10,
        step=5,
        help="选择本次测验的题目数量"
    )
    
    # 筛选题目
    filtered_questions = [
        q for q in questions
        if q["category"] in selected_categories and q["difficulty"] in selected_difficulty
    ]
    
    st.info(f"📊 符合条件的题目：{len(filtered_questions)} 道")
    
    # 开始按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 开始测验", use_container_width=True, type="primary"):
            if len(filtered_questions) < num_questions:
                st.error(f"符合条件的题目不足 {num_questions} 道，请调整筛选条件！")
            else:
                # 随机选择题目
                st.session_state.selected_questions = random.sample(filtered_questions, num_questions)
                st.session_state.current_question_idx = 0
                st.session_state.user_answers = {}
                st.session_state.quiz_started = True
                st.session_state.quiz_finished = False
                st.session_state.show_explanation = False
                st.rerun()


def render_quiz_question():
    """渲染当前题目"""
    
    questions = st.session_state.selected_questions
    current_idx = st.session_state.current_question_idx
    current_question = questions[current_idx]
    
    # 进度条
    progress = (current_idx + 1) / len(questions)
    st.markdown(f"""
        <div class="progress-bar-custom">
            <div class="progress-fill-custom" style="width: {progress * 100}%"></div>
        </div>
        <p style="text-align: center; color: #666; margin-top: 0.5rem;">
            进度：{current_idx + 1} / {len(questions)}
        </p>
    """, unsafe_allow_html=True)
    
    # 题目卡片
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    
    # 题目头部
    difficulty_class = {
        "简单": "difficulty-simple",
        "中等": "difficulty-medium",
        "困难": "difficulty-hard"
    }[current_question["difficulty"]]
    
    st.markdown(f"""
        <div class="question-header">
            <span class="question-number">第 {current_idx + 1} 题</span>
            <div>
                <span class="question-category">{current_question["category"]}</span>
                <span class="question-difficulty {difficulty_class}">{current_question["difficulty"]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 题目内容
    st.markdown(f'<div class="question-text">❓ {current_question["question"]}</div>', unsafe_allow_html=True)
    
    # 选项
    user_answered = current_question["id"] in st.session_state.user_answers
    
    for i, option in enumerate(current_question["options"]):
        is_correct = i == current_question["correct_answer"]
        
        # 如果已回答，显示正确/错误状态
        if user_answered:
            user_choice = st.session_state.user_answers[current_question["id"]]
            if i == user_choice:
                if is_correct:
                    st.success(f"✅ {chr(65+i)}. {option}")
                else:
                    st.error(f"❌ {chr(65+i)}. {option}")
            elif is_correct:
                st.success(f"✅ {chr(65+i)}. {option}")
            else:
                st.write(f"{chr(65+i)}. {option}")
        else:
            # 未回答，显示选项按钮
            if st.button(f"{chr(65+i)}. {option}", key=f"option_{i}", use_container_width=True):
                st.session_state.user_answers[current_question["id"]] = i
                st.session_state.show_explanation = True
                st.rerun()
    
    # 如果已回答，显示解析
    if user_answered and st.session_state.show_explanation:
        st.markdown(f"""
            <div class="explanation-box">
                <div class="explanation-title">💡 题目解析</div>
                <p>{current_question["explanation"]}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 底部按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_idx > 0:
            if st.button("⬅️ 上一题", use_container_width=True):
                st.session_state.current_question_idx -= 1
                st.session_state.show_explanation = current_question["id"] in st.session_state.user_answers
                st.rerun()
    
    with col3:
        if current_idx < len(questions) - 1:
            if st.button("下一题 ➡️", use_container_width=True):
                st.session_state.current_question_idx += 1
                next_question = questions[current_idx + 1]
                st.session_state.show_explanation = next_question["id"] in st.session_state.user_answers
                st.rerun()
        else:
            if st.button("📊 提交测验", use_container_width=True, type="primary"):
                st.session_state.quiz_finished = True
                st.rerun()


def render_quiz_results():
    """渲染测验结果"""
    
    questions = st.session_state.selected_questions
    user_answers = st.session_state.user_answers
    
    # 计算得分
    correct_count = sum(
        1 for q in questions
        if q["id"] in user_answers and user_answers[q["id"]] == q["correct_answer"]
    )
    total_count = len(questions)
    score_percentage = (correct_count / total_count * 100) if total_count > 0 else 0
    
    # 评价
    if score_percentage >= 90:
        message = "🎉 太棒了！你是排球战术大师！"
        emoji = "🏆"
    elif score_percentage >= 70:
        message = "👍 很好！继续加油！"
        emoji = "⭐"
    elif score_percentage >= 60:
        message = "💪 不错，还有提升空间！"
        emoji = "📈"
    else:
        message = "📚 多多学习，你会更好！"
        emoji = "💡"
    
    # 结果卡片
    st.markdown(f"""
        <div class="result-card">
            <div style="font-size: 5rem;">{emoji}</div>
            <div class="result-score">{score_percentage:.0f}分</div>
            <div class="result-message">{message}</div>
            
            <div class="result-details">
                <div class="stat-item">
                    <div class="stat-value">{correct_count}</div>
                    <div class="stat-label">答对题数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{total_count - correct_count}</div>
                    <div class="stat-label">答错题数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{total_count}</div>
                    <div class="stat-label">总题数</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 详细答题情况
    st.markdown("### 📋 详细答题情况")
    
    for idx, question in enumerate(questions):
        with st.expander(f"第 {idx + 1} 题 - {question['category']} ({question['difficulty']})"):
            st.markdown(f"**题目：** {question['question']}")
            
            if question["id"] in user_answers:
                user_choice = user_answers[question["id"]]
                correct_choice = question["correct_answer"]
                
                st.write(f"**你的答案：** {chr(65+user_choice)}. {question['options'][user_choice]}")
                st.write(f"**正确答案：** {chr(65+correct_choice)}. {question['options'][correct_choice]}")
                
                if user_choice == correct_choice:
                    st.success("✅ 回答正确")
                else:
                    st.error("❌ 回答错误")
                
                st.info(f"**解析：** {question['explanation']}")
            else:
                st.warning("⚠️ 未作答")
    
    # 操作按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 重新开始", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.current_question_idx = 0
            st.session_state.selected_questions = []
            st.session_state.user_answers = {}
            st.session_state.quiz_finished = False
            st.session_state.show_explanation = False
            st.rerun()
    
    with col3:
        if st.button("🏠 返回首页", use_container_width=True):
            # 清除所有quiz相关的session state
            for key in ["quiz_started", "current_question_idx", "selected_questions", 
                       "user_answers", "quiz_finished", "show_explanation"]:
                if key in st.session_state:
                    del st.session_state[key]
            
            # 返回首页
            st.session_state.page = "home"
            st.rerun()

