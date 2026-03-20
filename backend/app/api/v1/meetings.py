"""B-11, B-17: 会议纪要 API"""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.meeting import Meeting, MeetingDecision
from app.schemas.meeting import (
    MeetingCreate, MeetingUpdate, MeetingOut,
    MeetingDecisionCreate, MeetingDecisionOut,
)
from app.schemas.common import ResponseBase
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter()


@router.get("", response_model=ResponseBase)
async def list_meetings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    meeting_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """B-11: 获取会议列表"""
    query = select(Meeting)
    count_query = select(func.count()).select_from(Meeting)

    if meeting_type:
        query = query.where(Meeting.meeting_type == meeting_type)
        count_query = count_query.where(Meeting.meeting_type == meeting_type)

    total = (await db.execute(count_query)).scalar()
    items = (await db.execute(
        query.order_by(Meeting.meeting_time.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()

    return ResponseBase(data=paginate(page, page_size, total, [MeetingOut.model_validate(m) for m in items]))


@router.post("", response_model=ResponseBase, status_code=201)
async def create_meeting(
    body: MeetingCreate,
    db: AsyncSession = Depends(get_db),
):
    """B-11: 创建会议"""
    meeting = Meeting(**body.model_dump())
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    return ResponseBase(data=MeetingOut.model_validate(meeting))


@router.get("/{meeting_id}", response_model=ResponseBase)
async def get_meeting(meeting_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """B-11: 获取会议详情"""
    meeting = (await db.execute(select(Meeting).where(Meeting.id == meeting_id))).scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="会议不存在")
    return ResponseBase(data=MeetingOut.model_validate(meeting))


@router.put("/{meeting_id}", response_model=ResponseBase)
async def update_meeting(
    meeting_id: uuid.UUID, body: MeetingUpdate,
    db: AsyncSession = Depends(get_db),
):
    """B-11: 更新会议"""
    meeting = (await db.execute(select(Meeting).where(Meeting.id == meeting_id))).scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="会议不存在")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(meeting, key, value)

    await db.commit()
    await db.refresh(meeting)
    return ResponseBase(data=MeetingOut.model_validate(meeting))


@router.delete("/{meeting_id}", response_model=ResponseBase)
async def delete_meeting(meeting_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """B-11: 删除会议"""
    meeting = (await db.execute(select(Meeting).where(Meeting.id == meeting_id))).scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="会议不存在")
    await db.delete(meeting)
    await db.commit()
    return ResponseBase(message="删除成功")


# --- B-17: 会议决议 API ---


@router.get("/{meeting_id}/decisions", response_model=ResponseBase)
async def list_decisions(meeting_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """获取会议决议列表"""
    result = await db.execute(
        select(MeetingDecision).where(MeetingDecision.meeting_id == meeting_id)
        .order_by(MeetingDecision.created_at)
    )
    items = result.scalars().all()
    return ResponseBase(data=[MeetingDecisionOut.model_validate(d) for d in items])


@router.post("/{meeting_id}/decisions", response_model=ResponseBase, status_code=201)
async def create_decision(
    meeting_id: uuid.UUID, body: MeetingDecisionCreate,
    db: AsyncSession = Depends(get_db),
):
    """B-17: 创建会议决议"""
    decision = MeetingDecision(meeting_id=meeting_id, **body.model_dump())
    db.add(decision)
    await db.commit()
    await db.refresh(decision)
    return ResponseBase(data=MeetingDecisionOut.model_validate(decision))


@router.put("/{meeting_id}/decisions/{decision_id}", response_model=ResponseBase)
async def update_decision(
    meeting_id: uuid.UUID, decision_id: uuid.UUID,
    is_resolved: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    """更新决议状态（标记已解决）"""
    decision = (await db.execute(
        select(MeetingDecision).where(
            MeetingDecision.id == decision_id,
            MeetingDecision.meeting_id == meeting_id,
        )
    )).scalar_one_or_none()
    if not decision:
        raise HTTPException(status_code=404, detail="决议不存在")

    if is_resolved is not None:
        decision.is_resolved = is_resolved
        decision.resolved_at = datetime.utcnow() if is_resolved else None

    await db.commit()
    return ResponseBase(data=MeetingDecisionOut.model_validate(decision))


@router.delete("/{meeting_id}/decisions/{decision_id}", response_model=ResponseBase)
async def delete_decision(
    meeting_id: uuid.UUID, decision_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """删除决议"""
    decision = (await db.execute(
        select(MeetingDecision).where(
            MeetingDecision.id == decision_id,
            MeetingDecision.meeting_id == meeting_id,
        )
    )).scalar_one_or_none()
    if not decision:
        raise HTTPException(status_code=404, detail="决议不存在")
    await db.delete(decision)
    await db.commit()
    return ResponseBase(message="删除成功")
