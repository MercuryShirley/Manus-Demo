# 🎯 Manus 项目 - 快速参考卡片

## 项目信息

**项目名称**: Manus AI Chat Assistant  
**项目类型**: 多智能体 AI 聊天助手  
**技术栈**: FastAPI + DeepSeek + React-like Frontend  
**部署方式**: 本地 / Docker / Vercel  

---

## 🚀 一键启动

### macOS/Linux
```bash
chmod +x run.sh && ./run.sh
```

### Windows
```bash
run.bat
```

### Docker
```bash
export DEEPSEEK_API_KEY=your_key && docker-compose up --build
```

---

## 📝 必要配置

```bash
cd backend
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

获取 API Key: https://platform.deepseek.com/

---

## 🏗️ 项目架构

```
用户输入
  ↓
Planner (规划) → 任务拆解
  ↓
Executor (执行) → 并行处理
  ↓
Verify (验证) → 结果优化
  ↓
SSE 流式响应
```

---

## 📂 关键文件

| 文件 | 说明 |
|------|------|
| `backend/main.py` | FastAPI 主应用 |
| `backend/api/index.py` | Vercel 入口点 |
| `frontend/index.html` | 前端界面 |
| `vercel.json` | Vercel 配置 |
| `docker-compose.yml` | Docker 配置 |

---

## 🔗 重要链接

- 📖 [README.md](README.md) - 完整文档
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - 部署指南
- ⚡ [QUICKSTART.md](QUICKSTART.md) - 快速开始
- ✅ [CHECKLIST.md](CHECKLIST.md) - 检查清单

---

## 💻 常用命令

```bash
# 启动后端
uvicorn main:app --reload

# 启动前端服务器
python -m http.server 8080

# Docker 启动
docker-compose up --build

# Docker 停止
docker-compose down

# 本地测试 Vercel
vercel dev

# 部署到 Vercel
vercel deploy
```

---

## 🎤 面试讲述模板

> "这是一个**多智能体 AI 聊天助手**项目。
> 
> 核心创新是**三层智能体架构**：
> - **Planner** 分析问题并拆解任务
> - **Executor** 并行执行任务（搜索、分析等）
> - **Verify** 校验和优化最终结果
> 
> 技术上使用 **FastAPI** 和**异步编程**，支持 **SSE 流式响应**。
> 
> 部署方面支持**本地开发、Docker、Vercel** 多种方式。
> 
> 这个项目展示了我在**系统设计、工程实践、部署能力**方面的综合素质。"

---

## ❓ 常见问题速答

**Q: 如何获取 API Key?**  
A: 访问 https://platform.deepseek.com/ 注册后创建

**Q: 前端无法连接?**  
A: 确保后端运行在 localhost:8000，或检查 Vercel 部署

**Q: 搜索不工作?**  
A: 检查网络连接，搜索使用 DuckDuckGo 无需 API Key

**Q: 如何部署到 Vercel?**  
A: Push 到 GitHub → Vercel 导入 → 添加环境变量 → Deploy

---

## ✨ 项目亮点

✅ 清晰的架构设计  
✅ 完整的错误处理  
✅ 详细的文档  
✅ 多种部署方式  
✅ 优秀的用户体验  
✅ 生产级别的代码质量  

---

## 📊 项目统计

- 后端代码: ~1000 行
- 前端代码: ~500 行
- 文档: ~1500 行
- 配置文件: 6 个
- 支持部署方式: 3 种

---

## 🎯 下一步行动

1. ✅ 配置 .env 文件
2. ✅ 本地测试
3. ✅ 推送到 GitHub
4. ✅ 部署到 Vercel
5. ✅ 准备面试演示

---

**准备好了吗？开始部署吧！** 🚀
