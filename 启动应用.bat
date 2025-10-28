@echo off
chcp 65001 >nul
echo ========================================
echo 🏐 排球AI训练系统 - 启动脚本
echo ========================================
echo.

REM 激活conda环境
echo [1/2] 正在激活 volleyball 虚拟环境...
call conda activate volleyball
if %errorlevel% neq 0 (
    echo ❌ 错误: 无法激活 volleyball 环境
    echo 请先运行 "首次安装.bat" 创建环境
    pause
    exit /b 1
)
echo ✅ 环境激活成功
echo.

REM 启动streamlit应用
echo [2/2] 正在启动应用...
echo.
echo 🌐 浏览器将自动打开 http://localhost:8501
echo 💡 按 Ctrl+C 可停止服务
echo ========================================
echo.
streamlit run app.py

pause

