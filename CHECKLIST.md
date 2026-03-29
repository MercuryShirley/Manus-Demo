# ✅ Manus 部署检查清单

## 📋 本地开发准备

- [ ] 获取 DeepSeek API Key
  - 访问 https://platform.deepseek.com/
  - 注册账号并创建 API Key
  
- [ ] 配置环境变量
  ```bash
  cd backend
  cp .env.example .env
  # 编辑 .env，填入 DEEPSEEK_API_KEY
  ```

- [ ] 启动项目
  ```bash
  # macOS/Linux
  chmod +x run.sh
  ./run.sh
  
  # Windows
  run.bat
  
  # 或手动启动
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  uvicorn main:app --reload
  ```

- [ ] 测试前端
  - 打开 `frontend/index.html`
  - 或运行 `python -m http.server 8080`
  - 访问 `http://localhost:8080`

- [ ] 测试功能
  - [ ] 发送简单问题（如"你好"）
  - [ ] 发送需要搜索的问题
  - [ ] 检查任务进度显示
  - [ ] 检查最终回答显示

---

## 🐳 Docker 部署准备

- [ ] 安装 Docker 和 Docker Compose
  - https://www.docker.com/products/docker-desktop

- [ ] 测试 Docker 部署
  ```bash
  export DEEPSEEK_API_KEY=your_key_here
  docker-compose up --build
  ```

- [ ] 验证服务
  - 访问 `http://localhost:8000`
  - 检查 API 是否响应

---

## ☁️ Vercel 部署准备

### 步骤 1: GitHub 准备

- [ ] 初始化 Git 仓库
  ```bash
  git init
  git add .
  git commit -m "Initial commit: Manus AI Chat Assistant"
  ```

- [ ] 创建 GitHub 仓库
  - 访问 https://github.com/new
  - 创建新仓库 `manus`

- [ ] 推送代码
  ```bash
  git branch -M main
  git remote add origin https://github.com/your-username/manus.git
  git push -u origin main
  ```

### 步骤 2: Vercel 部署

- [ ] 访问 Vercel Dashboard
  - https://vercel.com/dashboard

- [ ] 导入项目
  - 点击 "New Project"
  - 选择 "Import Git Repository"
  - 搜索并选择 `manus` 仓库

- [ ] 配置项目
  - Project Name: `manus` (或自定义)
  - Framework Preset: `Other`
  - Root Directory: `./`

- [ ] 添加环境变量
  - 在 "Environment Variables" 部分
  - 名称: `DEEPSEEK_API_KEY`
  - 值: 你的 DeepSeek API Key

- [ ] 部署
  - 点击 "Deploy" 按钮
  - 等待部署完成（通常 2-5 分钟）

- [ ] 验证部署
  - [ ] 访问部署 URL（如 https://manus.vercel.app）
  - [ ] 测试聊天功能
  - [ ] 检查浏览器控制台是否有错误

### 步骤 3: 自定义域名（可选）

- [ ] 添加自定义域名
  - 在 Vercel 项目设置中找到 "Domains"
  - 添加你的域名
  - 按照说明配置 DNS 记录

---

## 🔍 部署后验证

### 功能测试

- [ ] 基本聊天
  - 发送 "你好"
  - 验证收到回复

- [ ] 搜索功能
  - 发送需要搜索的问题（如 "2024年最新的 AI 技术有哪些？"）
  - 验证搜索结果显示

- [ ] 任务进度
  - 验证任务规划显示
  - 验证任务执行进度
  - 验证最终结果显示

- [ ] UI/UX
  - [ ] 消息显示正确
  - [ ] Markdown 渲染正确
  - [ ] 表格显示正确
  - [ ] 代码块显示正确

### 性能测试

- [ ] 响应时间
  - 简单问题：< 5 秒
  - 搜索问题：< 15 秒

- [ ] 错误处理
  - [ ] 网络错误时显示错误信息
  - [ ] API 错误时显示错误信息
  - [ ] 无法连接时显示错误信息

---

## 📊 监控和维护

### 日志检查

- [ ] 本地开发
  - 检查后端控制台输出
  - 检查浏览器控制台错误

- [ ] Vercel 部署
  - 访问 Vercel 项目的 "Deployments" 标签
  - 查看部署日志
  - 查看函数日志

### 性能监控

- [ ] Vercel Analytics
  - 在 Vercel 项目设置中启用 Analytics
  - 监控页面加载时间
  - 监控 API 响应时间

- [ ] 错误监控
  - 设置错误告警
  - 定期检查错误日志

---

## 🚨 常见问题排查

### 问题 1: API Key 错误

**症状**: 提示 "API Key not configured"

**排查步骤**:
- [ ] 检查 `.env` 文件是否存在
- [ ] 检查 API Key 是否正确复制（无多余空格）
- [ ] 验证 API Key 是否有效
- [ ] 重启后端服务

### 问题 2: 前端无法连接后端

**症状**: 无法发送消息，控制台显示 CORS 错误

**排查步骤**:
- [ ] 本地开发：确保后端运行在 `http://localhost:8000`
- [ ] Vercel 部署：检查 API 路由是否正确
- [ ] 检查浏览器控制台错误信息
- [ ] 检查网络连接

### 问题 3: 搜索功能不工作

**症状**: 搜索任务失败

**排查步骤**:
- [ ] 检查网络连接
- [ ] 尝试手动访问 DuckDuckGo
- [ ] 查看后端日志中的错误信息
- [ ] 检查是否被 IP 限制

### 问题 4: Vercel 部署失败

**症状**: 部署显示 "Build failed"

**排查步骤**:
- [ ] 查看 Vercel 部署日志
- [ ] 检查 `requirements.txt` 是否完整
- [ ] 检查环境变量是否正确设置
- [ ] 检查 Python 版本兼容性

---

## 📝 文档检查

- [ ] README.md - 完整且最新
- [ ] DEPLOYMENT.md - 部署说明清晰
- [ ] QUICKSTART.md - 快速开始指南完整
- [ ] 代码注释充分
- [ ] API 文档完整

---

## 🎯 面试准备

- [ ] 准备项目演示
  - [ ] 本地运行演示
  - [ ] Vercel 部署演示
  - [ ] 功能演示

- [ ] 准备讲述要点
  - [ ] 架构设计说明
  - [ ] 技术栈介绍
  - [ ] 工程实践总结
  - [ ] 部署方案说明

- [ ] 准备回答问题
  - [ ] 为什么选择这个架构？
  - [ ] 如何处理错误？
  - [ ] 如何优化性能？
  - [ ] 如何扩展功能？

---

## ✨ 最终检查

- [ ] 所有文件已创建
- [ ] 所有配置已完成
- [ ] 本地测试通过
- [ ] Docker 测试通过
- [ ] Vercel 部署成功
- [ ] 所有功能正常工作
- [ ] 文档完整清晰
- [ ] 代码质量良好

---

## 🎉 完成！

当所有项目都打勾后，你的项目就完全准备好了！

**下一步**:
1. 推送到 GitHub
2. 部署到 Vercel
3. 分享给面试官
4. 准备讲述项目

**祝你面试顺利！** 🚀
