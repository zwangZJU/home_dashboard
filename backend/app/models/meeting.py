"""会议模型"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Enum, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class MeetingType(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    review = "review"
    other = "other"


class Meeting(Base, TimestampMixin, IDMixin):
    __tablename__ = "meetings"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    meeting_type: Mapped[MeetingType] = mapped_column(Enum(MeetingType), nullable=False)
    meeting_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="会议时间")
    duration_minutes: Mapped[int] = mapped_column(nullable=False, comment="时长(分钟)")
    host_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    participants: Mapped[list] = mapped_column(JSON, nullable=False, default=list, comment="参与人 ID 列表")
    content: Mapped[str] = mapped_column(Text, nullable=False, default="", comment="纪要正文")

    host = relationship("User")
    decisions = relationship(
        "MeetingDecision", back_populates="meeting",
        order_by="MeetingDecision.created_at", cascade="all, delete-orphan"
    )


class MeetingDecision(Base, TimestampMixin, IDMixin):
    __tablename__ = "meeting_decisions"

    meeting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("meetings.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False, comment="决议内容")
    is_resolved: Mapped[bool] = mapped_column(default=False, nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, comment="解决时间")
    related_task_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("tasks.id"), comment="关联任务")

    meeting = relationship("Meeting", back_populates="decisions")
