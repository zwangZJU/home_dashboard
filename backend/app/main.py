"""DevTrack 后端 - FastAPI 入口"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, requirements, tasks, meetings, progress, admin, dashboard
from app.config import settings
from app.models import Base
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时自动建表，关闭时释放资源"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="DevTrack API",
    description="开发项目全流程展示系统",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(requirements.router, prefix="/api/v1/requirements", tags=["需求管理"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["任务管理"])
app.include_router(meetings.router, prefix="/api/v1/meetings", tags=["会议纪要"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["进度展示"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["仪表盘"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["系统管理"])


@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {"code": 0, "message": "success", "data": {"status": "ok"}}
