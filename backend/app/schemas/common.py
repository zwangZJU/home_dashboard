"""统一响应模型"""
from typing import Any, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    """统一响应格式"""
    code: int = 0
    message: str = "success"
    data: T | None = None


class PaginatedData(BaseModel, Generic[T]):
    """分页数据"""
    total: int
    items: list[T]


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = 1
    page_size: int = 20
