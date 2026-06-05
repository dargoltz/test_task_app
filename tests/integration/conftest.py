import uuid
from datetime import datetime
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.api.app import app
from src.api.dependencies import get_task_service
from src.domain.value_objects import TaskPriority, TaskStatus
from src.schemas.response import TaskResponse, PageResponse


@pytest.fixture
def task_id():
    return uuid.uuid4()


@pytest.fixture
def task_response(task_id):
    return TaskResponse(
        id=task_id,
        name="Test task",
        description="Test description",
        priority=TaskPriority.LOW,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        started_at=None,
        finished_at=None,
        result=None,
        error=None,
    )


@pytest.fixture
def page_response(task_response):
    return PageResponse(
        page=1,
        limit=100,
        total=1,
        items=[task_response],
    )


@pytest.fixture
def task_service_mock():
    return AsyncMock()


@pytest_asyncio.fixture
async def client(task_service_mock):
    app.dependency_overrides[get_task_service] = lambda: task_service_mock

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
