"""工具函数：分页"""
from math import ceil


def paginate(page: int, page_size: int, total: int, items: list) -> dict:
    """分页工具，返回标准分页结构"""
    page = max(1, page)
    page_size = max(1, min(page_size, 100))
    offset = (page - 1) * page_size
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": ceil(total / page_size) if total > 0 else 0,
        "items": items,
    }
