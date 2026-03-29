# 🚀 Manus 快速参考指南

## 📋 项目概览

**Manus** 是一个基于 FastAPI 和 DeepSeek 的多智能体 AI 聊天助手。

- 🤖 三层智能体架构（Planner → Executor → Verify）
- 💬 实时流式响应
- 🔍 集成搜索功能
- ☁️ 支持 Vercel、Docker 部署

---

## ⚡ 5 分钟快速开始

### 1️⃣ 获取 API Key

访问 [DeepSeek 官网](https://platform.deepseek.com/)，创建 API Key

### 2️⃣ 配置环境

```bash
cd backend
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY
```

### 3️⃣ 启动项目

**macOS/Linux：**
```bash
chmod +x run.sh
./run.sh
```

**Windows：**
```bash
run.bat
```

**或手动启动：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 4️⃣ 打开前端

在浏览器打开 `frontend/index.html`

---

## 🐳 Docker 快速启动

```bash
export DEEPSEEK_API_KEY=your_key_here
docker-compose up --build
```

访问 `http://localhost:8000`

---

## ☁️ Vercel 部署（3 步）

### 1. 推送到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/manus.git
git push -u origin main
```

### 2. 连接 Vercel

访问 [Vercel Dashboard](https://vercel.com/dashboard)，导入你的 GitHub 仓库

### 3. 添加环境变量

在 Vercel 项目设置中添加：
```
DEEPSEEK_API_KEY = your_key_here
```

点击 Deploy，完成！

---

## 📁 项目结构

```
Manus/
├── backend/              # FastAPI 后端
│   ├── api/index.py     # Vercel 入口点
│   ├── main.py          # 主应用
│   ├── executor.py      # 执行智能体
│   ├── verifier.py      # 验证智能体
│   ├── prompts.py       # Planner 提示词
│   ├── tools.py         # 工具定义
│   └── requirements.txt
├── frontend/            # 前端
│   ├── index.html
│   ├── script.js
│   └── style.css
├── Dockerfile           # Docker 配置
├── docker-compose.yml   # Docker Compose
├── vercel.json          # Vercel 配置
├── run.sh              # Linux/macOS 启动脚本
├── run.bat             # Windows 启动脚本
├── README.md           # 项目文档
└── DEPLOYMENT.md       # 部署指南
```

---

## 🔧 常用命令

| 任务 | 命令 |
|------|------|
| 启动后端 | `uvicorn main:app --reload` |
| 启动前端服务器 | `python -m http.server 8080` |
| Docker 启动 | `docker-compose up --build` |
| Docker 停止 | `docker-compose down` |
| 本地测试 Vercel | `vercel dev` |
| 部署到 Vercel | `vercel deploy` |

---

## ❓ 常见问题

### Q: 如何获取 DeepSeek API Key？

A: 访问 https://platform.deepseek.com/，注册后在 API 管理页面创建

### Q: 前端无法连接后端？

A: 
- 本地开发：确保后端运行在 `http://localhost:8000`
- Vercel 部署：前端会自动使用 `/api/chat/stream`

### Q: 如何修改前端 UI？

A: 编辑 `frontend/style.css` 修改样式，`frontend/script.js` 修改逻辑

### Q: 支持哪些部署方式？

A: 支持本地开发、Docker、Docker Compose、Vercel、任何支持 Python 的云平台

---

## 📚 详细文档

- 📖 [README.md](README.md) - 完整项目文档
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - 详细部署指南
- 🤖 [FastAPI 文档](https://fastapi.tiangolo.com/)
- 🐳 [Docker 文档](https://docs.docker.com/)

---

## 🎯 下一步

1. ✅ 本地运行项目
2. ✅ 测试各种问题
3. ✅ 推送到 GitHub
4. ✅ 部署到 Vercel
5. ✅ 分享给面试官

---

## 💡 面试要点

当面试官问起这个项目时，重点讲述：

1. **架构设计**：三层智能体模式，展示系统设计能力
2. **技术栈**：FastAPI、异步编程、SSE 流式响应
3. **工程实践**：错误处理、日志、CORS、环境配置
4. **部署能力**：支持多种部署方式（本地、Docker、Vercel）
5. **用户体验**：实时任务进度、Markdown 渲染、流式响应

---

**祝你使用愉快！** 🎉
