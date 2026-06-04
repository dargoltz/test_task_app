import uuid
from datetime import datetime
from dataclasses import dataclass

from src.domain.value_objects import TaskPriority, TaskStatus


@dataclass
class Task:
    name: str
    description: str
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result: str | None = None
    error: str | None = None

    id: uuid.UUID | None = None
