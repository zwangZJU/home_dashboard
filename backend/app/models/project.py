"""项目模型"""
import enum
from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, IDMixin


class ProjectStatus(str, enum.Enum):
    active = "active"
    archived = "archived"


class Project(Base, TimestampMixin, IDMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="项目名称")
    description: Mapped[str | None] = mapped_column(Text, comment="项目描述")
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.active, nullable=False
    )
