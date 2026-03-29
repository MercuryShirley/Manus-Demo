# 🎯 Manus 项目 - 快速执行指南

## 📌 你的情况

- ✅ 项目已在 GitHub 上有一个版本
- ✅ 需要提交新的部署配置和文档
- ✅ 需要在本地运行项目
- ✅ 需要部署到 Vercel（只能提交前端链接）

---

## 1️⃣ 本地运行（5 分钟）

### 最快方式（推荐）

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

### 手动方式

```bash
# 1. 进入项目目录
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"

# 2. 配置环境变量
cd backend
cp .env.example .env
# 编辑 .env，填入你的 DEEPSEEK_API_KEY

# 3. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 4. 安装依赖
pip install -r requirements.txt

# 5. 启动后端
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 6. 在另一个终端打开前端
cd frontend
python -m http.server 8080
# 访问 http://localhost:8080
```

---

## 2️⃣ 提交到 GitHub（3 步）

### 步骤 1: 查看变更

```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
git status
```

你会看到：
- 修改的文件：README.md, frontend/script.js
- 新增的文件：11 个（部署配置、文档、脚本）

### 步骤 2: 添加所有文件

```bash
git add .
```

### 步骤 3: 提交并推送

```bash
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

### 一键执行

```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus" && \
git add . && \
git commit -m "feat: Add complete deployment configuration and documentation" && \
git push origin main
```

---

## 3️⃣ Vercel 部署配置（已修改）

### ✅ 已修改的 vercel.json

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

### 改进说明

| 改进 | 说明 |
|------|------|
| `maxDuration: 60` | 增加函数超时时间到 60 秒（默认 10 秒可能不够） |
| `rewrites` | 正确配置 API 路由重写 |
| `outputDirectory: "frontend"` | 前端文件会被正确部署为静态资源 |

### 部署步骤

1. **推送到 GitHub**
   ```bash
   git push origin main
   ```

2. **在 Vercel 导入项目**
   - 访问 https://vercel.com/dashboard
   - 点击 "New Project"
   - 选择你的 GitHub 仓库

3. **配置环境变量**
   - 在 Vercel 项目设置中找到 "Environment Variables"
   - 添加：`DEEPSEEK_API_KEY` = 你的 API Key

4. **部署**
   - 点击 "Deploy"
   - 等待部署完成（通常 2-5 分钟）

5. **获取前端链接**
   - 部署完成后，Vercel 会给你一个 URL
   - 例如：`https://manus.vercel.app`
   - 这就是你要提交的前端链接

---

## 🎯 完整流程（从现在开始）

### 第 1 步：本地测试（5 分钟）
```bash
./run.sh  # 或 run.bat
# 打开 frontend/index.html 测试
```

### 第 2 步：提交到 GitHub（1 分钟）
```bash
cd "/Users/zhangjiayi/Downloads/Vibe coding/Manus"
git add .
git commit -m "feat: Add complete deployment configuration and documentation"
git push origin main
```

### 第 3 步：部署到 Vercel（5 分钟）
1. 访问 https://vercel.com/dashboard
2. 导入你的 GitHub 仓库
3. 添加环境变量 `DEEPSEEK_API_KEY`
4. 点击 Deploy
5. 等待完成，获取前端链接

### 第 4 步：提交前端链接
- 获得的 Vercel URL 就是你要提交的前端链接
- 例如：`https://manus.vercel.app`

---

## ⚠️ 重要注意事项

### 关于后端 API

由于 Vercel 的限制，后端 API 会部署为 Serverless Functions：
- 每个请求的超时时间是 60 秒
- 长时间运行的任务可能会超时
- 如果需要更长的运行时间，考虑使用其他平台（如 Railway、Render）

### 关于前端链接

- 前端链接就是 Vercel 给你的主 URL
- 前端会自动连接到后端 API（`/api/chat/stream`）
- 不需要单独配置后端链接

### 关于 API Key

- 在 Vercel 环境变量中设置 `DEEPSEEK_API_KEY`
- 不要在代码中硬编码 API Key
- 不要在 GitHub 上提交 `.env` 文件（已在 .gitignore 中）

---

## 🔍 验证部署

### 本地验证
```bash
# 后端是否运行
curl http://localhost:8000/

# 前端是否可访问
# 打开 http://localhost:8080
```

### Vercel 验证
```bash
# 检查前端是否可访问
curl https://your-vercel-url.vercel.app/

# 检查 API 是否可访问
curl https://your-vercel-url.vercel.app/api/
```

---

## 📚 相关文档

- `README.md` - 完整项目文档
- `DEPLOYMENT.md` - 详细部署指南
- `QUICKSTART.md` - 快速参考
- `CHECKLIST.md` - 部署检查清单
- `QUICK_REFERENCE.md` - 快速参考卡片

---

## 💡 常见问题

**Q: 前端无法连接后端？**
A: 检查浏览器控制台，确保 API URL 正确（应该是 `/api/chat/stream`）

**Q: Vercel 部署失败？**
A: 查看 Vercel 部署日志，检查是否缺少环境变量或依赖

**Q: 本地运行时 API Key 错误？**
A: 确保 `.env` 文件存在且 API Key 正确

**Q: 如何修改前端 UI？**
A: 编辑 `frontend/style.css` 修改样式，`frontend/script.js` 修改逻辑

---

## ✨ 你已经准备好了！

现在就开始吧：

1. 运行 `./run.sh` 本地测试
2. 运行 `git push` 提交到 GitHub
3. 在 Vercel 部署
4. 获取前端链接提交

祝你成功！🚀
