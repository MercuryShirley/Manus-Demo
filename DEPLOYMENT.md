# 🚀 Manus 部署指南

## 目录

1. [本地开发](#本地开发)
2. [Docker 部署](#docker-部署)
3. [Vercel 部署](#vercel-部署)
4. [故障排查](#故障排查)

---

## 本地开发

### 前置要求

- Python 3.8+
- pip 包管理器
- DeepSeek API Key

### 步骤

#### 1. 获取 API Key

访问 [DeepSeek 官网](https://platform.deepseek.com/)：
1. 注册账号
2. 进入 API 管理页面
3. 创建新的 API Key
4. 复制 API Key

#### 2. 配置环境

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
```

#### 3. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

#### 4. 安装依赖

```bash
pip install -r requirements.txt
```

#### 5. 启动后端

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

你会看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 6. 打开前端

在浏览器中打开 `frontend/index.html`，或使用 Python 简单服务器：

```bash
cd frontend
python -m http.server 8080
```

然后访问 `http://localhost:8080`

---

## Docker 部署

### 前置要求

- Docker
- Docker Compose（可选）

### 方式 1：使用 Docker Compose（推荐）

最简单的方式，一条命令启动所有服务。

```bash
# 设置环境变量
export DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx

# 启动服务
docker-compose up --build

# 访问 http://localhost:8000
```

停止服务：
```bash
docker-compose down
```

### 方式 2：使用 Docker

```bash
# 构建镜像
docker build -t manus:latest .

# 运行容器
docker run -p 8000:8000 \
  -e DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx \
  manus:latest
```

### 方式 3：使用 Docker Hub（如果已发布）

```bash
docker run -p 8000:8000 \
  -e DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx \
  your-username/manus:latest
```

---

## Vercel 部署

Vercel 是最简单的云部署方式，支持自动部署和自定义域名。

### 前置要求

- GitHub 账号
- Vercel 账号（免费）
- DeepSeek API Key

### 步骤 1：推送到 GitHub

```bash
# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit: Manus AI Chat Assistant"

# 创建 GitHub 仓库并推送
git branch -M main
git remote add origin https://github.com/your-username/manus.git
git push -u origin main
```

### 步骤 2：连接 Vercel

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择 "Import Git Repository"
4. 搜索并选择你的 `manus` 仓库
5. 点击 "Import"

### 步骤 3：配置项目

在 Vercel 导入页面：

1. **Project Name**：保持默认或自定义
2. **Framework Preset**：选择 "Other"
3. **Root Directory**：保持默认（./）

### 步骤 4：添加环境变量

在 "Environment Variables" 部分：

| 名称 | 值 |
|------|-----|
| DEEPSEEK_API_KEY | sk-xxxxxxxxxxxxx |

### 步骤 5：部署

点击 "Deploy" 按钮，Vercel 会自动：
1. 克隆你的仓库
2. 安装依赖
3. 构建项目
4. 部署到 CDN

部署完成后，你会获得一个 URL，例如：
```
https://manus.vercel.app
```

### 步骤 6：配置自定义域名（可选）

1. 在 Vercel 项目设置中，找到 "Domains"
2. 添加你的自定义域名
3. 按照说明配置 DNS 记录

---

## 故障排查

### 问题 1：API Key 错误

**症状**：
```
DeepSeek API Key not configured
```

**解决方案**：
1. 检查 `.env` 文件是否存在
2. 确保 API Key 正确复制（没有多余空格）
3. 验证 API Key 是否有效（访问 DeepSeek 官网检查）
4. 重启后端服务

### 问题 2：前端无法连接后端

**症状**：
- 浏览器控制台显示 CORS 错误
- 无法发送消息

**解决方案**：

**本地开发**：
- 确保后端运行在 `http://localhost:8000`
- 检查防火墙设置

**Vercel 部署**：
- 前端会自动使用 `/api/chat/stream` 路由
- 检查 Vercel 部署日志中是否有错误

### 问题 3：搜索功能不工作

**症状**：
- 搜索任务失败
- 后端日志显示搜索错误

**解决方案**：
1. 检查网络连接
2. 尝试手动访问 DuckDuckGo 网站
3. 查看后端日志中的详细错误信息

### 问题 4：Vercel 部署失败

**症状**：
- 部署显示 "Build failed"
- 部署日志中有错误

**常见原因和解决方案**：

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `ModuleNotFoundError` | 缺少依赖 | 检查 `requirements.txt` 是否完整 |
| `DEEPSEEK_API_KEY not set` | 环境变量未配置 | 在 Vercel 项目设置中添加环境变量 |
| `Timeout` | 请求超时 | 增加 Vercel 函数超时时间 |

### 问题 5：本地测试 Vercel 部署

使用 Vercel CLI 在本地测试生产环境：

```bash
# 安装 Vercel CLI
npm i -g vercel

# 在项目根目录运行
vercel dev

# 访问 http://localhost:3000
```

---

## 性能优化建议

### 后端优化

1. **增加超时时间**：对于长时间运行的任务
   ```python
   async with httpx.AsyncClient(timeout=300.0) as client:
   ```

2. **添加缓存**：缓存搜索结果
   ```python
   from functools import lru_cache
   ```

3. **并行处理**：使用 asyncio 并行执行任务

### 前端优化

1. **压缩资源**：使用 gzip 压缩
2. **懒加载**：延迟加载非关键资源
3. **缓存**：使用浏览器缓存

### 部署优化

1. **使用 CDN**：加速静态资源
2. **启用 Gzip**：减少传输大小
3. **监控性能**：使用 Vercel Analytics

---

## 常用命令速查

```bash
# 本地开发
cd backend && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Docker
docker-compose up --build
docker-compose down

# Git
git add .
git commit -m "message"
git push origin main

# Vercel CLI
vercel deploy
vercel dev
vercel logs
```

---

## 获取帮助

- 📖 [FastAPI 文档](https://fastapi.tiangolo.com/)
- 🤖 [DeepSeek API 文档](https://platform.deepseek.com/docs)
- 🐳 [Docker 文档](https://docs.docker.com/)
- ☁️ [Vercel 文档](https://vercel.com/docs)

---

**祝你部署顺利！** 🎉
