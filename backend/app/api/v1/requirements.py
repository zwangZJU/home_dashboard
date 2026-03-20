"""B-09, B-12, B-13: 需求管理 API"""
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.requirement import Requirement, RequirementHistory
from app.schemas.requirement import RequirementCreate, RequirementUpdate, RequirementOut, RequirementHistoryOut
from app.schemas.common import ResponseBase
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter()


async def _generate_req_no(db: AsyncSession) -> str:
    """生成需求编号 REQ-XXX"""
    result = await db.execute(select(func.count()).select_from(Requirement))
    count = result.scalar() or 0
    return f"REQ-{count + 1:03d}"


async def _record_history(
    db: AsyncSession, req_id: uuid.UUID, action: str,
    old_val: dict | None, new_val: dict | None, operator_id: uuid.UUID,
):
    """写入需求变更记录"""
    history = RequirementHistory(
        requirement_id=req_id, action=action,
        old_value=old_val, new_value=new_val, operator_id=operator_id,
    )
    db.add(history)


@router.get("", response_model=ResponseBase)
async def list_requirements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    priority: str | None = None,
    parent_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    """B-09: 获取需求列表"""
    query = select(Requirement)
    count_query = select(func.count()).select_from(Requirement)

    if status:
        query = query.where(Requirement.status == status)
        count_query = count_query.where(Requirement.status == status)
    if priority:
        query = query.where(Requirement.priority == priority)
        count_query = count_query.where(Requirement.priority == priority)
    if parent_id is not None:
        query = query.where(Requirement.parent_id == parent_id)
        count_query = count_query.where(Requirement.parent_id == parent_id)
    else:
        # 默认只查顶级需求
        query = query.where(Requirement.parent_id.is_(None))
        count_query = count_query.where(Requirement.parent_id.is_(None))

    total = (await db.execute(count_query)).scalar()
    items = (await db.execute(
        query.order_by(Requirement.created_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()

    return ResponseBase(data=paginate(page, page_size, total, [RequirementOut.model_validate(r) for r in items]))


@router.post("", response_model=ResponseBase, status_code=201)
async def create_requirement(
    body: RequirementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """B-09: 创建需求"""
    req = Requirement(
        req_no=await _generate_req_no(db),
        title=body.title,
        description=body.description,
        priority=body.priority,
        status=body.status,
        proposer_id=current_user.id,
        expected_date=body.expected_date,
        parent_id=body.parent_id,
    )
    db.add(req)
    await db.flush()

    # B-13: 记录创建历史
    await _record_history(db, req.id, "create", None, req.title, current_user.id)
    await db.commit()
    await db.refresh(req)
    return ResponseBase(data=RequirementOut.model_validate(req))


@router.get("/{req_id}", response_model=ResponseBase)
async def get_requirement(req_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """B-09: 获取需求详情"""
    req = (await db.execute(select(Requirement).where(Requirement.id == req_id))).scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="需求不存在")
    return ResponseBase(data=RequirementOut.model_validate(req))


@router.put("/{req_id}", response_model=ResponseBase)
async def update_requirement(
    req_id: uuid.UUID, body: RequirementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """B-09: 更新需求（自动记录变更历史）"""
    req = (await db.execute(select(Requirement).where(Requirement.id == req_id))).scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="需求不存在")

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return ResponseBase(data=RequirementOut.model_validate(req))

    # B-13: 记录状态变更
    if "status" in update_data and update_data["status"] != req.status:
        await _record_history(
            db, req.id, "status_change",
            {"status": req.status.value}, {"status": update_data["status"].value},
            current_user.id,
        )

    for key, value in update_data.items():
        setattr(req, key, value)

    await db.commit()
    await db.refresh(req)
    return ResponseBase(data=RequirementOut.model_validate(req))


@router.delete("/{req_id}", response_model=ResponseBase)
async def delete_requirement(
    req_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """B-09: 删除需求"""
    req = (await db.execute(select(Requirement).where(Requirement.id == req_id))).scalar_one_or_none()
    if not req:
        raise HTTPException(status_code=404, detail="需求不存在")
    await db.delete(req)
    await db.commit()
    return ResponseBase(message="删除成功")


@router.get("/{req_id}/history", response_model=ResponseBase)
async def get_requirement_history(req_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """B-13: 获取需求变更记录"""
    result = await db.execute(
        select(RequirementHistory)
        .where(RequirementHistory.requirement_id == req_id)
        .order_by(RequirementHistory.created_at.desc())
    )
    items = result.scalars().all()
    return ResponseBase(data=[RequirementHistoryOut.model_validate(h) for h in items])
