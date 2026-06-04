import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.persistence.orm_models import Base


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    priority: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(DateTime)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    result: Mapped[str | None] = mapped_column(Text(), nullable=True)
    error: Mapped[str | None] = mapped_column(Text(), nullable=True)
