"""B-18: 仪表盘统计 API"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select, func, and_, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.requirement import Requirement
from app.models.task import Task
from app.models.meeting import Meeting
from app.schemas.common import ResponseBase

router = APIRouter()


@router.get("/stats", response_model=ResponseBase)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """B-18: 仪表盘统计数据"""
    today = datetime.now().date()

    # 总需求数
    total_reqs = (await db.execute(select(func.count()).select_from(Requirement))).scalar() or 0

    # 进行中任务数
    active_tasks = (await db.execute(
        select(func.count()).select_from(Task)
        .where(Task.status.in_(["in_progress", "testing"]))
    )).scalar() or 0

    # 已完成任务数
    completed_tasks = (await db.execute(
        select(func.count()).select_from(Task).where(Task.status == "done")
    )).scalar() or 0

    # 逾期任务数（截止日期 < 今天 且 状态不是 done）
    overdue_tasks = (await db.execute(
        select(func.count()).select_from(Task)
        .where(Task.due_date < today, Task.status != "done")
    )).scalar() or 0

    # 最近 30 天完成趋势
    thirty_days_ago = today - timedelta(days=30)
    trend_result = await db.execute(
        select(cast(Task.updated_at, Date), func.count())
        .where(Task.status == "done", cast(Task.updated_at, Date) >= thirty_days_ago)
        .group_by(cast(Task.updated_at, Date))
        .order_by(cast(Task.updated_at, Date))
    )
    trend_data = [{"date": str(row[0]), "count": row[1]} for row in trend_result.all()]

    # 最近 5 条会议
    recent_meetings_result = await db.execute(
        select(Meeting).order_by(Meeting.meeting_time.desc()).limit(5)
    )
    recent_meetings = [
        {
            "id": str(m.id), "title": m.title,
            "meeting_time": m.meeting_time.isoformat(),
            "participants": m.participants,
        }
        for m in recent_meetings_result.scalars().all()
    ]

    # 高优先级任务 Top 10
    urgent_tasks_result = await db.execute(
        select(Task).where(Task.priority == "high", Task.status != "done")
        .order_by(Task.due_date.asc().nullslast()).limit(10)
    )
    urgent_tasks = [
        {
            "id": str(t.id), "task_no": t.task_no, "title": t.title,
            "status": t.status.value, "due_date": str(t.due_date) if t.due_date else None,
        }
        for t in urgent_tasks_result.scalars().all()
    ]

    return ResponseBase(data={
        "total_requirements": total_reqs,
        "active_tasks": active_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
        "trend_data": trend_data,
        "recent_meetings": recent_meetings,
        "urgent_tasks": urgent_tasks,
    })
