@echo off
REM Manus 快速启动脚本 (Windows)

echo.
echo 🚀 Manus AI Chat Assistant - 快速启动
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python
    echo 请访问 https://www.python.org/downloads/ 安装 Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python 版本: %PYTHON_VERSION%
echo.

REM 进入 backend 目录
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查 .env 文件
if not exist ".env" (
    echo.
    echo ⚠️  未找到 .env 文件
    echo 请创建 .env 文件并添加你的 DeepSeek API Key：
    echo.
    echo   copy .env.example .env
    echo   REM 编辑 .env，填入你的 DEEPSEEK_API_KEY
    echo.
    pause
    exit /b 1
)

REM 检查 API Key
findstr /M "your_api_key_here" .env >nul
if not errorlevel 1 (
    echo.
    echo ❌ 错误：API Key 未配置
    echo 请编辑 .env 文件，将 'your_api_key_here' 替换为你的实际 API Key
    echo.
    pause
    exit /b 1
)

REM 安装依赖
echo 📚 安装依赖...
pip install -q -r requirements.txt

echo.
echo ✅ 所有准备就绪！
echo.
echo 🎯 启动后端服务...
echo 访问地址: http://localhost:8000
echo.
echo 💡 提示：
echo   - 在另一个终端打开 frontend/index.html
echo   - 或使用 Python 简单服务器: python -m http.server 8080
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 启动 FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
