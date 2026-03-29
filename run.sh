#!/bin/bash

# Manus 快速启动脚本

echo "🚀 Manus AI Chat Assistant - 快速启动"
echo "======================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请访问 https://www.python.org/downloads/ 安装 Python 3.8+"
    exit 1
fi

echo "✅ Python 版本: $(python3 --version)"
echo ""

# 进入 backend 目录
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  未找到 .env 文件"
    echo "请创建 .env 文件并添加你的 DeepSeek API Key："
    echo ""
    echo "  cp .env.example .env"
    echo "  # 编辑 .env，填入你的 DEEPSEEK_API_KEY"
    echo ""
    exit 1
fi

# 检查 API Key
if grep -q "your_api_key_here" .env; then
    echo ""
    echo "❌ 错误：API Key 未配置"
    echo "请编辑 .env 文件，将 'your_api_key_here' 替换为你的实际 API Key"
    echo ""
    exit 1
fi

# 安装依赖
echo "📚 安装依赖..."
pip install -q -r requirements.txt

echo ""
echo "✅ 所有准备就绪！"
echo ""
echo "🎯 启动后端服务..."
echo "访问地址: http://localhost:8000"
echo ""
echo "💡 提示："
echo "  - 在另一个终端打开 frontend/index.html"
echo "  - 或使用 Python 简单服务器: python -m http.server 8080"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动 FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
