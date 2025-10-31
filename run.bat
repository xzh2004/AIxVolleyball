@echo off
echo 🏐 启动排球AI训练系统...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 📦 检查依赖...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 📥 首次运行，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖检查完成
echo.
echo 🚀 启动Streamlit应用...
echo 📱 浏览器将自动打开 http://localhost:8501
echo 💡 按 Ctrl+C 停止服务器
echo.

streamlit run app.py

pause



