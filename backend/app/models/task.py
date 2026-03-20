"""任务模型"""
import uuid
import enum
from datetime import date
from sqlalchemy import String, Text, Enum, Date, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    testing = "testing"
    done = "done"


class TaskPriority(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Task(Base, TimestampMixin, IDMixin):
    __tablename__ = "tasks"

    task_no: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment="任务编号")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.todo, nullable=False
    )
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority), nullable=False)
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), comment="负责人")
    requirement_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("requirements.id"), comment="关联需求")
    parent_task_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("tasks.id"), comment="父任务")
    estimated_hours: Mapped[float | None] = mapped_column(Float, comment="预估工时")
    due_date: Mapped[date | None] = mapped_column(Date, comment="截止日期")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    # 关联
    assignee = relationship("User", back_populates="assigned_tasks")
    requirement = relationship("Requirement", back_populates="tasks")
    children = relationship("Task", backref="parent", remote_side="Task.id", lazy="selectin")
    subtasks = relationship("SubTask", back_populates="task", order_by="SubTask.sort_order", cascade="all, delete-orphan")
    comments = relationship("TaskComment", back_populates="task", order_by="TaskComment.created_at", cascade="all, delete-orphan")


class SubTask(Base, IDMixin):
    __tablename__ = "subtasks"

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_done: Mapped[bool] = mapped_column(default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    task = relationship("Task", back_populates="subtasks")


class TaskComment(Base, TimestampMixin, IDMixin):
    __tablename__ = "task_comments"

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    task = relationship("Task", back_populates="comments")
    user = relationship("User")
