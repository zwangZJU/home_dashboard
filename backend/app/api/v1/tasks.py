"""B-10, B-14, B-15, B-16: 任务管理 API"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.task import Task, SubTask, TaskComment
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskOut, SubTaskCreate, SubTaskOut,
    TaskCommentCreate, TaskCommentOut, TaskSortUpdate,
)
from app.schemas.common import ResponseBase
from app.utils.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter()


async def _generate_task_no(db: AsyncSession) -> str:
    """生成任务编号 TASK-XXX"""
    result = await db.execute(select(func.count()).select_from(Task))
    count = result.scalar() or 0
    return f"TASK-{count + 1:03d}"


@router.get("", response_model=ResponseBase)
async def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    priority: str | None = None,
    assignee_id: uuid.UUID | None = None,
    requirement_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    """B-10: 获取任务列表"""
    query = select(Task)
    count_query = select(func.count()).select_from(Task)

    if status:
        query = query.where(Task.status == status)
        count_query = count_query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
        count_query = count_query.where(Task.priority == priority)
    if assignee_id:
        query = query.where(Task.assignee_id == assignee_id)
        count_query = count_query.where(Task.assignee_id == assignee_id)
    if requirement_id:
        query = query.where(Task.requirement_id == requirement_id)
        count_query = count_query.where(Task.requirement_id == requirement_id)

    total = (await db.execute(count_query)).scalar()
    items = (await db.execute(
        query.order_by(Task.sort_order, Task.created_at.desc())
        .offset((page - 1) * page_size).limit(page_size)
    )).scalars().all()

    return ResponseBase(data=paginate(page, page_size, total, [TaskOut.model_validate(t) for t in items]))


@router.post("", response_model=ResponseBase, status_code=201)
async def create_task(
    body: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """B-10: 创建任务"""
    task = Task(
        task_no=await _generate_task_no(db),
        **body.model_dump(),
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return ResponseBase(data=TaskOut.model_validate(task))


@router.get("/{task_id}", response_model=ResponseBase)
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """B-10: 获取任务详情"""
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return ResponseBase(data=TaskOut.model_validate(task))


@router.put("/{task_id}", response_model=ResponseBase)
async def update_task(
    task_id: uuid.UUID, body: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    """B-10: 更新任务"""
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return ResponseBase(data=TaskOut.model_validate(task))


@router.delete("/{task_id}", response_model=ResponseBase)
async def delete_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """B-10: 删除任务"""
    task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    await db.delete(task)
    await db.commit()
    return ResponseBase(message="删除成功")


# --- B-14: 子任务 API ---


@router.get("/{task_id}/subtasks", response_model=ResponseBase)
async def list_subtasks(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """获取任务的子任务列表"""
    result = await db.execute(
        select(SubTask).where(SubTask.task_id == task_id).order_by(SubTask.sort_order)
    )
    items = result.scalars().all()
    return ResponseBase(data=[SubTaskOut.model_validate(s) for s in items])


@router.post("/{task_id}/subtasks", response_model=ResponseBase, status_code=201)
async def create_subtask(
    task_id: uuid.UUID, body: SubTaskCreate, db: AsyncSession = Depends(get_db),
):
    """创建子任务"""
    # 获取当前最大 sort_order
    result = await db.execute(
        select(func.count()).select_from(SubTask).where(SubTask.task_id == task_id)
    )
    order = result.scalar() or 0

    subtask = SubTask(
        task_id=task_id, title=body.title, is_done=body.is_done, sort_order=order,
    )
    db.add(subtask)
    await db.commit()
    await db.refresh(subtask)
    return ResponseBase(data=SubTaskOut.model_validate(subtask))


@router.put("/{task_id}/subtasks/{subtask_id}", response_model=ResponseBase)
async def update_subtask(
    task_id: uuid.UUID, subtask_id: uuid.UUID, body: SubTaskCreate,
    db: AsyncSession = Depends(get_db),
):
    """更新子任务（勾选完成等）"""
    subtask = (await db.execute(
        select(SubTask).where(SubTask.id == subtask_id, SubTask.task_id == task_id)
    )).scalar_one_or_none()
    if not subtask:
        raise HTTPException(status_code=404, detail="子任务不存在")

    subtask.title = body.title
    subtask.is_done = body.is_done
    await db.commit()
    return ResponseBase(data=SubTaskOut.model_validate(subtask))


@router.delete("/{task_id}/subtasks/{subtask_id}", response_model=ResponseBase)
async def delete_subtask(
    task_id: uuid.UUID, subtask_id: uuid.UUID, db: AsyncSession = Depends(get_db),
):
    """删除子任务"""
    subtask = (await db.execute(
        select(SubTask).where(SubTask.id == subtask_id, SubTask.task_id == task_id)
    )).scalar_one_or_none()
    if not subtask:
        raise HTTPException(status_code=404, detail="子任务不存在")
    await db.delete(subtask)
    await db.commit()
    return ResponseBase(message="删除成功")


# --- B-15: 任务评论 API ---


@router.get("/{task_id}/comments", response_model=ResponseBase)
async def list_comments(task_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """获取任务评论列表"""
    result = await db.execute(
        select(TaskComment).where(TaskComment.task_id == task_id).order_by(TaskComment.created_at)
    )
    items = result.scalars().all()
    return ResponseBase(data=[TaskCommentOut.model_validate(c) for c in items])


@router.post("/{task_id}/comments", response_model=ResponseBase, status_code=201)
async def create_comment(
    task_id: uuid.UUID, body: TaskCommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """添加任务评论"""
    comment = TaskComment(task_id=task_id, user_id=current_user.id, content=body.content)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return ResponseBase(data=TaskCommentOut.model_validate(comment))


# --- B-16: 拖拽排序 API ---


@router.put("/sort", response_model=ResponseBase)
async def batch_update_sort(body: TaskSortUpdate, db: AsyncSession = Depends(get_db)):
    """B-16: 批量更新任务排序"""
    for item in body.items:
        task_id = item.get("id")
        sort_order = item.get("sort_order", 0)
        # 同时支持状态更新（拖拽到不同列）
        new_status = item.get("status")

        if task_id:
            task = (await db.execute(select(Task).where(Task.id == task_id))).scalar_one_or_none()
            if task:
                task.sort_order = sort_order
                if new_status:
                    task.status = new_status

    await db.commit()
    return ResponseBase(message="排序更新成功")
