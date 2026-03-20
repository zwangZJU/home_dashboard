"""进度展示 Schema"""
from pydantic import BaseModel


class ProgressTimeline(BaseModel):
    """时间线数据（需求维度）"""
    items: list[dict]  # [{"id", "title", "status", "start_date", "end_date", "progress"}]


class BurndownData(BaseModel):
    """燃尽图数据"""
    ideal: list[dict]  # [{"date": ..., "remaining": ...}]
    actual: list[dict]


class MemberWorkload(BaseModel):
    """成员工作量统计"""
    items: list[dict]  # [{"user_id", "nickname", "total", "completed", "in_progress"}]
