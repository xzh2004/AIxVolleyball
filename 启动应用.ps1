# PowerShell 启动脚本
# 排球AI训练系统

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🏐 排球AI训练系统 - 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在正确目录
if (-not (Test-Path "app.py")) {
    Write-Host "❌ 错误: 找不到 app.py 文件" -ForegroundColor Red
    Write-Host "请确保在项目根目录运行此脚本" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 激活conda环境
Write-Host "[1/2] 正在激活 volleyball 虚拟环境..." -ForegroundColor Yellow

# 获取conda路径
$condaPath = Get-Command conda -ErrorAction SilentlyContinue
if ($null -eq $condaPath) {
    # 尝试常见的conda安装路径
    $possiblePaths = @(
        "$env:USERPROFILE\anaconda3\Scripts\conda.exe",
        "$env:USERPROFILE\miniconda3\Scripts\conda.exe",
        "C:\ProgramData\anaconda3\Scripts\conda.exe",
        "C:\ProgramData\miniconda3\Scripts\conda.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $condaPath = $path
            break
        }
    }
}

if ($null -eq $condaPath) {
    Write-Host "❌ 错误: 找不到 conda" -ForegroundColor Red
    Write-Host "请确保已安装 Anaconda 或 Miniconda" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 激活环境
& conda activate volleyball
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 错误: 无法激活 volleyball 环境" -ForegroundColor Red
    Write-Host "请先运行 '首次安装.bat' 创建环境" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "✅ 环境激活成功" -ForegroundColor Green
Write-Host ""

# 启动应用
Write-Host "[2/2] 正在启动应用..." -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 浏览器将自动打开 http://localhost:8501" -ForegroundColor Cyan
Write-Host "💡 按 Ctrl+C 可停止服务" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

streamlit run app.py

Read-Host "按回车键退出"

