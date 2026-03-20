"""会议相关 Schema"""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.models.meeting import MeetingType


class MeetingCreate(BaseModel):
    title: str
    meeting_type: MeetingType
    meeting_time: datetime
    duration_minutes: int
    host_id: UUID
    participants: list[UUID] = []
    content: str = ""


class MeetingUpdate(BaseModel):
    title: str | None = None
    meeting_type: MeetingType | None = None
    meeting_time: datetime | None = None
    duration_minutes: int | None = None
    participants: list[UUID] | None = None
    content: str | None = None


class MeetingOut(BaseModel):
    id: UUID
    title: str
    meeting_type: MeetingType
    meeting_time: datetime
    duration_minutes: int
    host_id: UUID
    participants: list
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MeetingDecisionCreate(BaseModel):
    content: str
    related_task_id: UUID | None = None


class MeetingDecisionOut(BaseModel):
    id: UUID
    meeting_id: UUID
    content: str
    is_resolved: bool
    resolved_at: datetime | None
    related_task_id: UUID | None

    model_config = {"from_attributes": True}
