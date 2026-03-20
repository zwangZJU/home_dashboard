"""B-21: 系统管理 API - 项目和成员管理"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus
from app.schemas.common import ResponseBase
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter()


# --- 项目管理 ---


@router.get("/projects", response_model=ResponseBase)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取项目列表"""
    query = select(Project)
    count_query = select(func.count()).select_from(Project)
    total = (await db.execute(count_query)).scalar()
    items = (await db.execute(
        query.order_by(Project.created_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()
    return ResponseBase(data=paginate(page, page_size, total, list(items)))


@router.post("/projects", response_model=ResponseBase, status_code=201)
async def create_project(name: str, description: str | None = None, db: AsyncSession = Depends(get_db)):
    """创建项目"""
    project = Project(name=name, description=description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return ResponseBase(data={"id": str(project.id), "name": project.name, "status": project.status.value})


@router.put("/projects/{project_id}", response_model=ResponseBase)
async def update_project(
    project_id: uuid.UUID, name: str | None = None,
    description: str | None = None, status: ProjectStatus | None = None,
    db: AsyncSession = Depends(get_db),
):
    """更新项目"""
    project = (await db.execute(select(Project).where(Project.id == project_id))).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if status is not None:
        project.status = status
    await db.commit()
    return ResponseBase(data={"id": str(project.id), "name": project.name, "status": project.status.value})


# --- 成员管理 ---


@router.get("/members", response_model=ResponseBase)
async def list_members(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取成员列表"""
    query = select(User)
    count_query = select(func.count()).select_from(User)
    total = (await db.execute(count_query)).scalar()
    items = (await db.execute(
        query.order_by(User.created_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()

    from app.schemas.user import UserOut
    return ResponseBase(data=paginate(page, page_size, total, [UserOut.model_validate(u) for u in items]))


@router.put("/members/{user_id}/role", response_model=ResponseBase)
async def update_member_role(
    user_id: uuid.UUID, role: UserRole,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """修改成员角色"""
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="仅管理员可修改角色")

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.role = role
    await db.commit()
    return ResponseBase(data={"user_id": str(user.id), "role": role.value})


@router.delete("/members/{user_id}", response_model=ResponseBase)
async def delete_member(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除成员"""
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="仅管理员可删除成员")

    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    await db.delete(user)
    await db.commit()
    return ResponseBase(message="删除成功")
