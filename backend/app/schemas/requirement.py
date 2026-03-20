"""需求相关 Schema"""
from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

from app.models.requirement import RequirementPriority, RequirementStatus


class RequirementCreate(BaseModel):
    title: str
    description: str
    priority: RequirementPriority
    status: RequirementStatus = RequirementStatus.draft
    expected_date: date | None = None
    parent_id: UUID | None = None


class RequirementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: RequirementPriority | None = None
    status: RequirementStatus | None = None
    expected_date: date | None = None


class RequirementOut(BaseModel):
    id: UUID
    req_no: str
    title: str
    description: str
    priority: RequirementPriority
    status: RequirementStatus
    proposer_id: UUID
    expected_date: date | None
    parent_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RequirementHistoryOut(BaseModel):
    id: UUID
    requirement_id: UUID
    action: str
    old_value: dict | None
    new_value: dict | None
    operator_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
