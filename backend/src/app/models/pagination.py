from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    """Internal pagination result (ORM items)."""

    page: int
    limit: int
    total: int
    items: list[Any]


class PaginatedResponse(BaseModel, Generic[T]):
    """API response wrapper for paginated lists."""

    page: int
    limit: int
    total: int
    items: list[T]
