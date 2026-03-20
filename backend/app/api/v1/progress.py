"""B-20: 进度统计 API"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.requirement import Requirement
from app.models.task import Task
from app.models.user import User
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("/timeline", response_model=ResponseBase)
async def get_timeline(db: AsyncSession = Depends(get_db)):
    """B-20: 时间线数据（需求维度，含进度计算）"""
    result = await db.execute(
        select(Requirement).where(Requirement.parent_id.is_(None))
        .order_by(Requirement.created_at)
    )
    requirements = result.scalars().all()

    items = []
    for req in requirements:
        # 计算子需求完成进度
        total_children = len(req.children)
        done_children = sum(1 for c in req.children if c.status == "done")
        progress = (done_children / total_children * 100) if total_children > 0 else (
            100 if req.status == "done" else 0
        )

        # 关联任务的进度
        tasks_result = await db.execute(
            select(Task).where(Task.requirement_id == req.id)
        )
        tasks = tasks_result.scalars().all()
        total_tasks = len(tasks)
        done_tasks = sum(1 for t in tasks if t.status == "done")
        if total_tasks > 0 and total_children == 0:
            progress = done_tasks / total_tasks * 100

        end_date = req.expected_date or req.updated_at.date() if req.updated_at else None

        items.append({
            "id": str(req.id),
            "title": req.title,
            "req_no": req.req_no,
            "status": req.status.value,
            "priority": req.priority.value,
            "start_date": str(req.created_at.date()) if req.created_at else None,
            "end_date": str(end_date) if end_date else None,
            "progress": round(progress, 1),
            "total_tasks": total_tasks,
            "done_tasks": done_tasks,
        })

    return ResponseBase(data=items)


@router.get("/burndown", response_model=ResponseBase)
async def get_burndown(
    days: int = Query(30, ge=7, le=90),
    db: AsyncSession = Depends(get_db),
):
    """B-20: 燃尽图数据（按日聚合已完成任务数）"""
    today = datetime.now().date()
    start_date = today - timedelta(days=days)

    # 总任务数
    total = (await db.execute(select(func.count()).select_from(Task))).scalar() or 0

    # 每日完成任务数
    result = await db.execute(
        select(cast(Task.updated_at, Date), func.count())
        .where(Task.status == "done", cast(Task.updated_at, Date) >= start_date)
        .group_by(cast(Task.updated_at, Date))
        .order_by(cast(Task.updated_at, Date))
    )
    completed_by_date = {row[0]: row[1] for row in result.all()}

    # 构建理想线和实际线
    ideal, actual = [], []
    remaining = total
    cumulative_done = 0

    for i in range(days + 1):
        d = start_date + timedelta(days=i)
        # 理想线：匀速递减
        ideal_remaining = max(0, round(total - (total / days) * i, 1))
        ideal.append({"date": str(d), "remaining": ideal_remaining})

        # 实际线
        if d in completed_by_date:
            cumulative_done += completed_by_date[d]
        actual_remaining = max(0, total - cumulative_done)
        actual.append({"date": str(d), "remaining": actual_remaining})

    return ResponseBase(data={"ideal": ideal, "actual": actual, "total": total})


@router.get("/member-workload", response_model=ResponseBase)
async def get_member_workload(db: AsyncSession = Depends(get_db)):
    """B-20: 成员工作量统计"""
    users_result = await db.execute(select(User))
    users = users_result.scalars().all()

    items = []
    for user in users:
        tasks_result = await db.execute(
            select(Task).where(Task.assignee_id == user.id)
        )
        tasks = tasks_result.scalars().all()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == "done")
        in_progress = sum(1 for t in tasks if t.status in ("in_progress", "testing"))

        items.append({
            "user_id": str(user.id),
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "todo": total - completed - in_progress,
        })

    # 按总任务数降序
    items.sort(key=lambda x: x["total"], reverse=True)
    return ResponseBase(data=items)
