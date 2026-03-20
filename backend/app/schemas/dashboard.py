"""仪表盘统计 Schema"""
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_requirements: int
    active_tasks: int
    completed_tasks: int
    overdue_tasks: int
    trend_data: list[dict]  # [{"date": "2026-03-20", "count": 3}]
    recent_meetings: list[dict]  # [{"id": ..., "title": ..., "meeting_time": ..., "participants": [...]}]
    urgent_tasks: list[dict]  # 高优先级任务 Top 10
