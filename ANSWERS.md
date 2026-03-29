# 🎯 三个问题的完整答案

## ❓ 问题 1: 本地运行的步骤

### 最快方式（推荐）- 30 秒启动

**macOS/Linux：**
```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
chmod +x run.sh
./run.sh
```

**Windows：**
```bash
cd "C:\Users\zhangjiayi\Downloads\Vibe coding\Manus"
run.bat
```

然后在浏览器打开 `frontend/index.html`

### 详细步骤（如果脚本不工作）

```bash
# 1. 进入项目目录
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"

# 2. 配置环境变量
cd backend
cp .env.example .env
# 用文本编辑器打开 .env，填入你的 DEEPSEEK_API_KEY

# 3. 创建虚拟环境
python -m venv venv

# 4. 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 5. 安装依赖
pip install -r requirements.txt

# 6. 启动后端
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 7. 在另一个终端打开前端
cd frontend
python -m http.server 8080
# 访问 http://localhost:8080
```

---

## ❓ 问题 2: 提交到 GitHub 的指令

### 一键提交（推荐）

```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
git add .
git commit -m "feat: Add complete deployment configuration and documentation

- Add Vercel deployment config (vercel.json) with Python 3.11 runtime
- Add Docker support (Dockerfile, docker-compose.yml)
- Add environment variable example (.env.example)
- Add Vercel Serverless entry point (backend/api/index.py)
- Add comprehensive documentation (README, DEPLOYMENT, QUICKSTART, CHECKLIST, QUICK_REFERENCE)
- Add automated startup scripts (run.sh, run.bat)
- Update frontend script.js to support multi-environment deployment
- Update README.md with complete documentation and deployment guide"
git push origin main
```

### 分步提交

```bash
# 1. 查看变更
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
git status

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "feat: Add complete deployment configuration and documentation"

# 4. 推送
git push origin main
```

### 简化版提交

```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus" && \
git add . && \
git commit -m "feat: Add deployment configuration and documentation" && \
git push origin main
```

---

## ❓ 问题 3: Vercel 部署文件修改

### ✅ 已修改的 vercel.json

**修改内容：**
- ✅ 添加了 `maxDuration: 60` - 增加函数超时时间到 60 秒
- ✅ 保持了 `rewrites` 配置 - 正确的 API 路由重写
- ✅ 保持了 `outputDirectory: "frontend"` - 前端文件正确部署

**完整配置：**
```json
{
  "buildCommand": "pip install -r backend/requirements.txt",
  "outputDirectory": "frontend",
  "env": {
    "DEEPSEEK_API_KEY": "@deepseek_api_key"
  },
  "functions": {
    "backend/api/index.py": {
      "runtime": "python3.11",
      "maxDuration": 60
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/backend/api/index.py"
    }
  ]
}
```

### 为什么这样配置？

| 配置项 | 作用 | 原因 |
|--------|------|------|
| `buildCommand` | 安装 Python 依赖 | 后端需要依赖 |
| `outputDirectory` | 前端文件位置 | 前端是静态资源 |
| `maxDuration: 60` | 函数超时时间 | 默认 10 秒不够，AI 任务需要更长时间 |
| `rewrites` | API 路由转发 | 前端请求 `/api/*` 转发到后端 |
| `runtime: python3.11` | Python 版本 | 后端使用 Python 3.11 |

---

## 🚀 完整部署流程

### 第 1 步：本地测试（5 分钟）

```bash
./run.sh  # 或 run.bat
# 打开 frontend/index.html 测试
```

### 第 2 步：提交到 GitHub（1 分钟）

```bash
git add .
git commit -m "feat: Add deployment configuration"
git push origin main
```

### 第 3 步：部署到 Vercel（5 分钟）

1. 访问 https://vercel.com/dashboard
2. 点击 "New Project"
3. 选择你的 GitHub 仓库
4. 在 "Environment Variables" 中添加：
   - 名称：`DEEPSEEK_API_KEY`
   - 值：你的 DeepSeek API Key
5. 点击 "Deploy"

### 第 4 步：获取前端链接

部署完成后，Vercel 会给你一个 URL，例如：
```
https://manus.vercel.app
```

这就是你要提交的前端链接！

---

## 📊 当前状态

### Git 变更

```
修改的文件 (2 个):
  • README.md
  • frontend/script.js

新增的文件 (13 个):
  • CHECKLIST.md
  • DEPLOYMENT.md
  • DEPLOYMENT_GUIDE.md
  • QUICKSTART.md
  • QUICK_REFERENCE.md
  • START_HERE.md
  • Dockerfile
  • docker-compose.yml
  • run.bat
  • run.sh
  • vercel.json (已修改)
  • backend/.env.example
  • backend/api/index.py
```

### 文件大小

```
总大小: ~50 KB
文档行数: 超过 1500 行
代码行数: 295 行 (Vercel 入口点)
```

---

## 💡 关键要点

### 关于前端链接

✅ 前端链接就是 Vercel 给你的主 URL  
✅ 不需要单独配置后端链接  
✅ 前端会自动连接到后端 API（`/api/chat/stream`）

### 关于后端 API

✅ 后端部署为 Vercel Serverless Functions  
✅ 超时时间已设置为 60 秒  
✅ 前端请求 `/api/*` 会自动转发到后端

### 关于 API Key

✅ 在 Vercel 环境变量中设置 `DEEPSEEK_API_KEY`  
✅ 不要在代码中硬编码 API Key  
✅ 不要在 GitHub 上提交 `.env` 文件

---

## 📚 相关文档

| 文档 | 用途 |
|------|------|
| `START_HERE.md` | 快速开始指南 ⭐ |
| `README.md` | 完整项目文档 |
| `DEPLOYMENT.md` | 详细部署指南 |
| `DEPLOYMENT_GUIDE.md` | 部署配置说明 |
| `QUICKSTART.md` | 快速参考 |
| `CHECKLIST.md` | 部署检查清单 |
| `QUICK_REFERENCE.md` | 快速参考卡片 |

---

## ✨ 现在就开始吧！

### 立即执行

```bash
# 1. 本地测试
./run.sh

# 2. 提交到 GitHub
git add . && git commit -m "feat: Add deployment config" && git push

# 3. 部署到 Vercel
# 访问 https://vercel.com/dashboard 导入仓库

# 4. 获取前端链接
# 部署完成后提交 Vercel URL
```

---

**祝你成功！** 🚀
