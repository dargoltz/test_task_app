from enum import Enum


class TaskStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
