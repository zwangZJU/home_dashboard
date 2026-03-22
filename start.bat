@echo off
echo ========================================
echo   DevTrack 一键启动（无需 Docker）
echo ========================================
echo.

cd /d %~dp0

:: ---- 后端 ----
echo [1/2] 启动后端...
cd backend
if not exist .env copy .env.example .env >nul 2>&1

:: 检查 python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 没有找到 python，请先安装 Python 3.10+
    pause
    exit /b 1
)

:: 安装依赖
pip install -r requirements.txt -q

:: 后台启动后端
start /b uvicorn app.main:app --host 0.0.0.0 --port 8000 > ..\api.log 2>&1
echo        后端启动中 (端口 8000)...

:: 等后端就绪
:wait_api
timeout /t 2 /nobreak >nul
curl -s http://localhost:8000/api/v1/health >nul 2>&1
if %errorlevel% neq 0 goto wait_api
echo        后端已就绪！

:: ---- 前端 ----
echo [2/2] 启动前端...
cd ..\frontend

where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 没有找到 node，请先安装 Node.js 18+
    pause
    exit /b 1
)

if not exist node_modules npm install

start /b npm run dev > ..\web.log 2>&1

echo.
echo ========================================
echo   启动成功！
echo   前端地址: http://localhost:3000
echo   API 文档: http://localhost:8000/docs
echo ========================================
echo.
echo   停止服务: 关闭本窗口，或运行 stop.bat
echo   后端日志: api.log
echo   前端日志: web.log
echo.
pause
