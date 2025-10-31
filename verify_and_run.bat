@echo off
REM 验证FFmpeg并启动应用的便捷脚本
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       🔍 验证 FFmpeg 并启动应用                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM 检查FFmpeg
echo 🔍 检查 FFmpeg 安装...
ffmpeg -version > nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ FFmpeg 已安装！
    echo.
    ffmpeg -version | findstr "ffmpeg version"
    echo.
    echo ════════════════════════════════════════════════════════════
    echo   ✨ 太好了！现在视频将完美在浏览器中播放
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 🚀 正在启动 Streamlit...
    echo.
    streamlit run app.py
) else (
    echo ❌ FFmpeg 未安装
    echo.
    echo ════════════════════════════════════════════════════════════
    echo   📥 请先安装 FFmpeg
    echo ════════════════════════════════════════════════════════════
    echo.
    echo 方法1（推荐）:
    echo   conda install ffmpeg
    echo.
    echo 方法2:
    echo   conda install -c conda-forge ffmpeg
    echo.
    echo 方法3:
    echo   choco install ffmpeg
    echo.
    echo 安装完成后，重新运行此脚本。
    echo.
    echo 📖 详细说明: INSTALL_FFMPEG.md
    echo.
    pause
)

