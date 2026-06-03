import uuid
from datetime import datetime
from dataclasses import dataclass

from src.domain.value_objects import TaskPriority, TaskStatus


@dataclass
class Task:
    id: uuid.UUID
    name: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    result: str | None
    error: str | None
