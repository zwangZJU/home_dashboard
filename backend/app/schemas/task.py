"""任务相关 Schema"""
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: TaskPriority
    status: TaskStatus = TaskStatus.todo
    assignee_id: UUID | None = None
    requirement_id: UUID | None = None
    parent_task_id: UUID | None = None
    estimated_hours: float | None = None
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    assignee_id: UUID | None = None
    requirement_id: UUID | None = None
    estimated_hours: float | None = None
    due_date: date | None = None


class TaskOut(BaseModel):
    id: UUID
    task_no: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee_id: UUID | None
    requirement_id: UUID | None
    parent_task_id: UUID | None
    estimated_hours: float | None
    due_date: date | None
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SubTaskCreate(BaseModel):
    title: str
    is_done: bool = False


class SubTaskOut(BaseModel):
    id: UUID
    task_id: UUID
    title: str
    is_done: bool
    sort_order: int

    model_config = {"from_attributes": True}


class TaskCommentCreate(BaseModel):
    content: str


class TaskCommentOut(BaseModel):
    id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskSortUpdate(BaseModel):
    """批量更新排序"""
    items: list[dict]  # [{"id": uuid, "sort_order": int}]
