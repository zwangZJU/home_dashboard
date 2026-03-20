"""用户模型"""
import uuid
import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, IDMixin


class UserRole(str, enum.Enum):
    admin = "admin"
    member = "member"


class User(Base, TimestampMixin, IDMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, comment="昵称")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="邮箱")
    avatar_url: Mapped[str | None] = mapped_column(String(500), comment="头像 URL")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希")
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.member, nullable=False, comment="角色"
    )

    # 关联
    proposed_requirements = relationship("Requirement", back_populates="proposer", foreign_keys="Requirement.proposer_id")
    assigned_tasks = relationship("Task", back_populates="assignee")
