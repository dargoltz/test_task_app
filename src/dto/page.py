from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Page(Generic[T]):
    items: list[T]
    total: int
