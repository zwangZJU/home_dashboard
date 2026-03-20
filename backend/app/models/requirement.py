"""需求模型"""
import uuid
import enum
from datetime import date, datetime
from sqlalchemy import String, Text, Enum, Date, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class RequirementPriority(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class RequirementStatus(str, enum.Enum):
    draft = "draft"
    review = "review"
    approved = "approved"
    in_dev = "in_dev"
    done = "done"


class Requirement(Base, TimestampMixin, IDMixin):
    __tablename__ = "requirements"

    req_no: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, comment="需求编号")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="标题")
    description: Mapped[str] = mapped_column(Text, nullable=False, comment="描述")
    priority: Mapped[RequirementPriority] = mapped_column(Enum(RequirementPriority), nullable=False)
    status: Mapped[RequirementStatus] = mapped_column(
        Enum(RequirementStatus), default=RequirementStatus.draft, nullable=False
    )
    proposer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    expected_date: Mapped[date | None] = mapped_column(Date, comment="预计上线日期")
    parent_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("requirements.id"), comment="父需求 ID")

    # 关联
    proposer = relationship("User", back_populates="proposed_requirements", foreign_keys=[proposer_id])
    children = relationship("Requirement", backref="parent", remote_side="Requirement.id", lazy="selectin")
    history = relationship("RequirementHistory", back_populates="requirement", order_by="RequirementHistory.created_at.desc()")
    tasks = relationship("Task", back_populates="requirement")


class RequirementHistory(Base, TimestampMixin, IDMixin):
    __tablename__ = "requirement_histories"

    requirement_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("requirements.id"), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False, comment="操作类型")
    old_value: Mapped[dict | None] = mapped_column(JSON, comment="变更前值")
    new_value: Mapped[dict | None] = mapped_column(JSON, comment="变更后值")
    operator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    requirement = relationship("Requirement", back_populates="history")
