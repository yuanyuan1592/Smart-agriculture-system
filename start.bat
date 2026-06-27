@echo off
REM Start both backend and frontend for the Smart Agriculture System.
REM 使用前请确保已安装 Node.js 和 Python，并已在 frontend/backend 目录安装依赖。

SETLOCAL
cd /d %~dp0

where py >nul 2>&1
if %errorlevel%==0 (
  set "PYTHON=py"
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    set "PYTHON=python"
  ) else (
    echo 未找到 Python 可执行文件，请安装 Python 并确保 py 或 python 在 PATH 中。
    exit /b 1
  )
)

where npm >nul 2>&1
if %errorlevel% neq 0 (
  echo 未找到 npm，请安装 Node.js 并确保 npm 在 PATH 中。
  exit /b 1
)

echo 正在启动后端服务...
start "Backend" %PYTHON% backend\main.py

echo 正在启动前端开发服务器...
start "Frontend" npm --prefix frontend run dev

echo.
echo 后端应运行于 http://localhost:8000
echo 前端应运行于 http://localhost:5173
ENDLOCAL
