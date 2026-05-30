import datetime
import uuid
from typing import Optional

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.enums import TaskPriority, TaskStatus


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority, name="task_priority"))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus, name="task_status"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    result: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
