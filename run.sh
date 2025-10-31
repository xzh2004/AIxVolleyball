#!/bin/bash

echo "🏐 启动排球AI训练系统..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未检测到Python，请先安装Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "📥 首次运行，正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

echo "✅ 依赖检查完成"
echo ""
echo "🚀 启动Streamlit应用..."
echo "📱 浏览器将自动打开 http://localhost:8501"
echo "💡 按 Ctrl+C 停止服务器"
echo ""

streamlit run app.py



