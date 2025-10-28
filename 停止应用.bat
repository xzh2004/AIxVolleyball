@echo off
chcp 65001 >nul
echo ========================================
echo 🛑 停止 Streamlit 应用
echo ========================================
echo.

REM 查找并关闭streamlit进程
tasklist | findstr /i "streamlit" >nul
if %errorlevel% equ 0 (
    echo 正在关闭 Streamlit 进程...
    taskkill /f /im streamlit.exe 2>nul
    taskkill /f /fi "WINDOWTITLE eq streamlit*" 2>nul
    echo ✅ 应用已停止
) else (
    echo ℹ️  没有运行中的 Streamlit 应用
)

echo.
pause

