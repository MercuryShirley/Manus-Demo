# Manus-Demo

一个基于 FastAPI 和 DeepSeek 的多智能体 AI 聊天助手演示项目。

## 🎯 项目特色

- 🤖 **Planner 智能体**：任务规划与拆解
- ⚙️ **Executor 智能体**：任务执行与工具调用
- ✅ **Verify 智能体**：回答校验与优化
- 🔍 **搜索工具**：集成 DuckDuckGo 搜索
- 💬 **实时交互**：SSE 流式响应
- 🚀 **云部署就绪**：支持 Vercel、Docker 部署

## 📊 架构设计

```
用户输入
   ↓
[Planner 智能体] → 任务规划与拆解
   ↓
[Executor 智能体] → 并行执行子任务（搜索/分析）
   ↓
[Verify 智能体] → 结果校验与优化
   ↓
流式返回给前端
```

## 🛠 技术栈

- **后端**：FastAPI, DeepSeek API, httpx, Python 3.11+
- **前端**：HTML, CSS, JavaScript (原生)
- **AI 模型**：DeepSeek R1 (Reasoner), DeepSeek Chat
- **部署**：Vercel, Docker, Docker Compose

## 🚀 快速开始

### 前置要求

- Python 3.8+
- DeepSeek API Key（[获取](https://platform.deepseek.com/)）

### 本地开发

#### 1. 克隆项目

```bash
git clone <your-repo-url>
cd Manus
```

#### 2. 配置环境

```bash
cd backend
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY
```

#### 3. 启动后端

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. 打开前端

在浏览器中打开 `frontend/index.html`，或使用 Live Server：

```bash
# 使用 Python 简单服务器
cd frontend
python -m http.server 8080
# 访问 http://localhost:8080
```

## 🐳 Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 设置环境变量
export DEEPSEEK_API_KEY=your_api_key_here

# 启动服务
docker-compose up --build

# 访问 http://localhost:8000
```

### 使用 Docker

```bash
# 构建镜像
docker build -t manus:latest .

# 运行容器
docker run -p 8000:8000 \
  -e DEEPSEEK_API_KEY=your_api_key_here \
  manus:latest
```

## ☁️ Vercel 部署

### 步骤 1：推送到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo>
git push -u origin main
```

### 步骤 2：连接 Vercel

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入你的 GitHub 仓库
4. 选择项目根目录

### 步骤 3：配置环境变量

在 Vercel 项目设置中，添加环境变量：

```
DEEPSEEK_API_KEY = your_deepseek_api_key_here
```

### 步骤 4：部署

点击 "Deploy"，Vercel 会自动构建并部署你的项目。

部署完成后，你会获得一个 URL，例如：`https://manus.vercel.app`

## 📁 项目结构

```
Manus/
├── backend/
│   ├── api/
│   │   └── index.py          # Vercel Serverless 入口点
│   ├── main.py               # FastAPI 主应用
│   ├── executor.py           # Executor 智能体
│   ├── verifier.py           # Verify 智能体
│   ├── prompts.py            # Planner 提示词
│   ├── tools.py              # 工具定义
│   ├── search_tool.py        # 搜索工具实现
│   ├── config.py             # 配置管理
│   ├── requirements.txt      # Python 依赖
│   ├── .env.example          # 环境变量示例
│   └── .env                  # 环境变量（本地）
├── frontend/
│   ├── index.html            # 聊天界面
│   ├── script.js             # 前端逻辑
│   └── style.css             # 样式
├── Dockerfile                # Docker 配置
├── docker-compose.yml        # Docker Compose 配置
├── vercel.json               # Vercel 配置
├── README.md                 # 项目文档
└── .gitignore                # Git 忽略文件
```

## 🧠 智能体架构详解

### Planner 智能体

负责分析用户问题，将其拆解为可执行的子任务序列，并确定任务依赖关系。

**输出格式**：JSON 结构，包含：
- `query_analysis`：对用户问题的理解
- `subtasks`：子任务列表，每个任务包含 id、name、description、type、tool、tool_input、depends_on

### Executor 智能体

负责执行 Planner 规划的子任务，包括：
- 调用工具（如搜索）
- 进行分析推理
- 整合结果生成初步回答

### Verify 智能体

负责校验和优化 Executor 生成的回答，确保：
- 完整性：没有被截断
- 准确性：准确回答了用户问题
- 格式正确：Markdown 格式规范

## 🔧 常见问题

### Q: 提示 API Key 错误？

**A:** 检查以下几点：
1. 确保 `.env` 文件存在且正确配置
2. 确保 API Key 有效（访问 [DeepSeek 官网](https://platform.deepseek.com/) 检查）
3. 本地开发时，重启后端服务
4. Vercel 部署时，检查环境变量是否正确设置

### Q: 前端无法连接后端？

**A:** 
- 本地开发：确保后端运行在 `http://localhost:8000`
- Vercel 部署：前端会自动使用 `/api/chat/stream` 路由
- 检查浏览器控制台的错误信息

### Q: 搜索功能不工作？

**A:** 搜索使用 DuckDuckGo，无需 API Key。如果不工作：
1. 检查网络连接
2. 查看后端日志中的错误信息
3. 尝试手动访问 DuckDuckGo 网站

### Q: 如何本地测试 Vercel 部署？

**A:** 使用 Vercel CLI：

```bash
npm i -g vercel
vercel dev
```

## 📝 API 文档

### 流式聊天接口

**POST** `/chat/stream`

请求体：
```json
{
  "message": "你的问题"
}
```

响应：SSE 流式事件

事件类型：
- `status`：处理状态
- `plan`：任务规划
- `task_start`：任务开始
- `task_complete`：任务完成
- `final`：最终结果
- `done`：处理完成

### 非流式聊天接口

**POST** `/chat`

请求体：
```json
{
  "message": "你的问题"
}
```

响应：
```json
{
  "reply": "回答内容",
  "reasoning_content": "推理过程（可选）",
  "plan": {
    "query_analysis": "问题分析",
    "subtasks": [...]
  }
}
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT
