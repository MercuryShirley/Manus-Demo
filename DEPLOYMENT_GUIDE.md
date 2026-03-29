# 🚀 Manus 项目 - 本地运行 + GitHub 提交 + Vercel 部署完整指南

## 📋 当前状态

✅ 项目已在 GitHub 上有一个版本  
✅ 新增了 11 个文件（部署配置、文档、脚本）  
✅ 修改了 2 个文件（README.md、frontend/script.js）  

---

## 1️⃣ 本地运行步骤（详细版）

### 前置要求
- Python 3.8+
- DeepSeek API Key（[获取](https://platform.deepseek.com/)）

### 步骤 1: 配置环境变量

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：
```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
```

### 步骤 2: 创建虚拟环境

```bash
cd backend
python -m venv venv
```

### 步骤 3: 激活虚拟环境

**macOS/Linux：**
```bash
source venv/bin/activate
```

**Windows：**
```bash
venv\Scripts\activate
```

### 步骤 4: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 5: 启动后端

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

你会看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 步骤 6: 打开前端

在浏览器中打开：
```
frontend/index.html
```

或使用 Python 简单服务器（在另一个终端）：
```bash
cd frontend
python -m http.server 8080
```

然后访问 `http://localhost:8080`

### 快速启动（一键脚本）

**macOS/Linux：**
```bash
chmod +x run.sh
./run.sh
```

**Windows：**
```bash
run.bat
```

---

## 2️⃣ 提交到 GitHub 的指令

### 查看当前状态
```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
git status
```

### 添加所有新文件和修改

```bash
git add .
```

### 提交更改

```bash
git commit -m "feat: Add complete deployment configuration

- Add Vercel deployment config (vercel.json)
- Add Docker support (Dockerfile, docker-compose.yml)
- Add environment variable example (.env.example)
- Add Vercel Serverless entry point (backend/api/index.py)
- Add comprehensive documentation (README, DEPLOYMENT, QUICKSTART, CHECKLIST, QUICK_REFERENCE)
- Add automated startup scripts (run.sh, run.bat)
- Update frontend script.js to support multi-environment deployment
- Update README.md with complete documentation"
```

### 推送到 GitHub

```bash
git push origin main
```

### 完整命令（一次性）

```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
git add .
git commit -m "feat: Add complete deployment configuration

- Add Vercel deployment config (vercel.json)
- Add Docker support (Dockerfile, docker-compose.yml)
- Add environment variable example (.env.example)
- Add Vercel Serverless entry point (backend/api/index.py)
- Add comprehensive documentation (README, DEPLOYMENT, QUICKSTART, CHECKLIST, QUICK_REFERENCE)
- Add automated startup scripts (run.sh, run.bat)
- Update frontend script.js to support multi-environment deployment
- Update README.md with complete documentation"
git push origin main
```

---

## 3️⃣ Vercel 部署文件分析 & 修改建议

### 当前 vercel.json 的问题

你的 `vercel.json` 配置有一个问题：**Vercel 不支持 Python 作为前端框架**。

当前配置：
```json
{
  "buildCommand": "pip install -r backend/requirements.txt",
  "outputDirectory": "frontend",
  "functions": {
    "backend/api/index.py": {
      "runtime": "python3.11"
    }
  }
}
```

**问题**：
- `outputDirectory: "frontend"` 告诉 Vercel 前端在 `frontend` 目录
- 但 Vercel 会尝试构建前端，而前端只是静态 HTML/CSS/JS
- 这会导致部署失败

### ✅ 修改后的 vercel.json

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

**改进点**：
1. ✅ 添加了 `maxDuration: 60` - 增加函数超时时间（默认 10 秒可能不够）
2. ✅ 添加了 `rewrites` - 正确配置 API 路由重写
3. ✅ 保持 `outputDirectory: "frontend"` - 前端文件会被正确部署

让我为你更新这个文件：
