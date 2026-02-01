# Manus-Demo

一个基于 FastAPI 和 DeepSeek 的多智能体 AI 聊天助手演示项目。

## 功能特性

- 🤖 **Planner 智能体**：任务规划与拆解
- ⚙️ **Executor 智能体**：任务执行与工具调用
- ✅ **Verify 智能体**：回答校验与优化
- 🔍 **搜索工具**：集成 DuckDuckGo 搜索
- 💬 **实时交互**：SSE 流式响应

## 技术栈

- **后端**：FastAPI, DeepSeek API, httpx
- **前端**：HTML, CSS, JavaScript
- **AI 模型**：DeepSeek R1 (Reasoner), DeepSeek Chat

## 快速开始

### 后端设置

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 配置环境变量

创建 `backend/.env` 文件：

```
DEEPSEEK_API_KEY=your_api_key_here
```

### 启动后端

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

直接在浏览器中打开 `frontend/index.html`

## 项目结构

```
Manus-Demo/
├── backend/
│   ├── main.py          # FastAPI 主应用
│   ├── executor.py      # Executor 智能体
│   ├── verifier.py      # Verify 智能体
│   ├── prompts.py       # Planner 提示词
│   ├── tools.py         # 工具定义
│   ├── search_tool.py   # 搜索工具实现
│   └── config.py        # 配置管理
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

## 智能体架构

### Planner 智能体
负责分析用户问题，将其拆解为可执行的子任务序列，并确定任务依赖关系。

### Executor 智能体
负责执行 Planner 规划的子任务，包括调用工具（如搜索）和整合结果生成初步回答。

### Verify 智能体
负责校验和优化 Executor 生成的回答，确保完整性、准确性和格式正确。

## License

MIT
