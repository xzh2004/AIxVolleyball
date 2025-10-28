@echo off
chcp 65001 >nul
echo ========================================
echo 🏐 排球AI训练系统 - 首次安装脚本
echo ========================================
echo.
echo 此脚本将：
echo  1. 创建 volleyball 虚拟环境
echo  2. 安装所有依赖包
echo  3. 验证安装是否成功
echo.
echo 预计耗时: 5-10 分钟
echo ========================================
echo.
pause

REM 创建conda环境
echo [1/3] 正在创建 volleyball 虚拟环境 (Python 3.8)...
call conda create -n volleyball python=3.8 -y
if %errorlevel% neq 0 (
    echo ❌ 错误: 环境创建失败
    pause
    exit /b 1
)
echo ✅ 环境创建成功
echo.

REM 激活环境
echo [2/3] 正在安装依赖包...
call conda activate volleyball

REM 安装依赖（使用清华镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  使用镜像安装失败，尝试其他方式...
    pip install mediapipe opencv-python numpy streamlit pillow scipy -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
)

if %errorlevel% neq 0 (
    echo ❌ 错误: 依赖安装失败
    echo 请检查网络连接或参考 "手动安装指南.md"
    pause
    exit /b 1
)
echo ✅ 依赖安装成功
echo.

REM 验证安装
echo [3/3] 正在验证安装...
python -c "import mediapipe; print('✅ MediaPipe: OK')"
python -c "import cv2; print('✅ OpenCV: OK')"
python -c "import streamlit; print('✅ Streamlit: OK')"
python -c "import numpy; print('✅ NumPy: OK')"
echo.

echo ========================================
echo 🎉 安装完成！
echo ========================================
echo.
echo 现在可以运行 "启动应用.bat" 启动系统
echo.
pause

