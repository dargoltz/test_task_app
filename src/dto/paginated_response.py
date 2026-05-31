from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total: int
    items: list[T]
