# DevTrack — 开发项目全流程展示系统

> 🚀 轻量级项目协作工具，让需求 → 任务 → 开发 → 交付的全过程透明可见

✨ **出品人：** 昭昭 | 🏀 **后端：** 球球 | 🎨 **前端：** 小团

---

## 📖 项目简介

DevTrack 是一个面向研发团队的**全流程项目管理平台**，把散落在文档、聊天、表格里的信息集中到一个地方。核心思路很简单——**让项目进度一眼可见，让团队协作不再靠猜**。

### 解决的痛点

| 😫 痛点 | ✅ DevTrack 的方案 |
|---------|-------------------|
| 需求散落各处，查起来费劲 | 需求集中管理，支持 Markdown 富文本与状态追踪 |
| 任务分配靠口头，进度不透明 | 可视化看板，拖拽即可更新状态 |
| 会议纪要没人看，决策容易忘 | 纪要关联项目，关键决策可追溯 |
| 各工具割裂，信息孤岛 | 一个系统覆盖需求、任务、会议、进度 |

---

## 🎯 功能模块

### 🏠 仪表盘（Dashboard）
项目全景总览：关键数据统计、快捷入口、一目了然的项目健康度。

### 📋 需求管理（Requirements）
- 需求创建与编辑（Markdown 富文本）
- 优先级与状态管理
- 需求详情与追踪

### ✅ 任务管理（Tasks）
- **拖拽式看板**：待办 → 进行中 → 测试中 → 已完成
- 任务分配给团队成员
- 优先级标签与状态徽章

### 📝 会议纪要（Meetings）
- 会议记录（Markdown 编辑器）
- 纪要列表与详情查看
- 关联项目与决策追踪

### 📊 进度展示（Progress）
- 项目进度统计与可视化
- 时间线与燃尽图（ECharts）
- 多维度数据图表

### ⚙️ 系统管理（Admin）
- 项目设置
- 成员管理

---

## 🛠 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | Vue 3 + TypeScript + Vite |
| **UI 框架** | Element Plus + Lucide Icons |
| **状态管理** | Pinia |
| **图表** | ECharts |
| **富文本** | md-editor-v3（Markdown） |
| **拖拽** | vuedraggable |
| **HTTP** | Axios |
| **后端** | FastAPI (Python) |
| **ORM** | SQLAlchemy 2.0 (async) |
| **数据库** | SQLite（默认）/ PostgreSQL（生产） |
| **认证** | JWT (python-jose + passlib) |

---

## 🚀 快速启动

### 环境要求

- **Python** ≥ 3.10
- **Node.js** ≥ 18
- **pnpm**（推荐）或 npm

### 1. 克隆项目

```bash
git clone https://github.com/zwangZJU/home_dashboard.git
cd home_dashboard
```

### 2. 启动后端

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 启动服务（默认端口 8000）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后可访问：
- 📡 API 文档：http://localhost:8000/docs
- 💓 健康检查：http://localhost:8000/api/v1/health

### 3. 启动前端

```bash
cd frontend

# 安装依赖
pnpm install
# 或 npm install

# 启动开发服务器（默认端口 5173）
pnpm dev
# 或 npm run dev
```

前端启动后访问：http://localhost:5173

### 4. 环境变量配置（可选）

在 `backend/` 目录下创建 `.env` 文件，按需覆盖默认配置：

```env
# 数据库（默认使用 SQLite）
DEVTRACK_DATABASE_URL=sqlite+aiosqlite:///./devtrack.db
# PostgreSQL 示例：
# DEVTRACK_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/devtrack

# JWT 密钥（生产环境务必修改！）
DEVTRACK_JWT_SECRET_KEY=your-secret-key-here
DEVTRACK_JWT_EXPIRE_MINUTES=1440

# CORS 允许的前端地址
DEVTRACK_CORS_ORIGINS=["http://localhost:5173"]
```

> 所有配置项使用 `DEVTRACK_` 前缀，详见 `backend/app/config.py`。

---

## 📁 项目结构

```
home_dashboard/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API 路由（auth, tasks, requirements, meetings, progress, dashboard, admin）
│   │   ├── models/          # SQLAlchemy 数据模型
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── services/        # 业务逻辑层
│   │   ├── utils/           # 工具函数（认证、分页）
│   │   ├── config.py        # 全局配置
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # FastAPI 入口
│   ├── tests/
│   ├── requirements.txt
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── *.vue            # 页面组件（Dashboard, TaskBoard, RequirementList, MeetingList 等）
│   │   ├── *.ts             # API 请求层、路由、状态管理
│   │   ├── App.vue
│   │   └── main.ts
│   └── package.json
└── docs/
    └── product-design.md    # 完整产品设计文档
```

---

## 📄 License

MIT

---

> 💡 **提示：** 完整的产品设计方案见 [`docs/product-design.md`](docs/product-design.md)，包含详细的需求分析、交互设计和数据模型。
