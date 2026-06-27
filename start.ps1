# Start both backend and frontend for the Smart Agriculture System.
# 使用前请确保已安装 Node.js 和 Python，并已在 frontend/backend 目录安装依赖。

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$pythonExe = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { $null }
if (-not $pythonExe) {
    Write-Host '未找到 Python，可执行文件。请安装 Python 并确保 py 或 python 在 PATH 中。' -ForegroundColor Red
    exit 1
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host '未找到 npm。请安装 Node.js 并确保 npm 在 PATH 中。' -ForegroundColor Red
    exit 1
}

Write-Host '正在启动后端服务...' -ForegroundColor Green
Start-Process -FilePath $pythonExe -ArgumentList '-3', 'backend/main.py' -WorkingDirectory "$scriptDir\backend" -NoNewWindow

Write-Host '正在启动前端开发服务器...' -ForegroundColor Green
Start-Process -FilePath npm -ArgumentList 'run', 'dev', '--prefix', 'frontend' -WorkingDirectory "$scriptDir\frontend" -NoNewWindow

Write-Host '后端应运行于 http://localhost:8000，前端应运行于 http://localhost:5173' -ForegroundColor Cyan
Write-Host '如果未自动打开窗口，请手动在 PowerShell 中运行 start.ps1' -ForegroundColor Yellow
