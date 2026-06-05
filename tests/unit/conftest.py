import uuid
import datetime

import pytest
from unittest.mock import Mock, AsyncMock

from src.domain.value_objects import TaskStatus, TaskPriority
from src.dto import Page
from src.schemas.request import TaskRequest
from src.service import TaskService


@pytest.fixture
def task():
    t = Mock()
    t.id = uuid.uuid4()
    t.name = "Test task"
    t.description = "Test description"
    t.created_at = datetime.datetime.now()
    t.status = TaskStatus.NEW
    t.priority = TaskPriority.LOW
    t.started_at = None
    t.finished_at = None
    t.result = None
    t.error = None
    return t


@pytest.fixture
def task_request():
    return TaskRequest(
        name="Test task",
        description="Test description",
        priority=TaskPriority.LOW,
    )


@pytest.fixture
def tasks_page(task):
    return Page(
        items=[task],
        total=1,
    )


@pytest.fixture
def repository():
    return AsyncMock()


@pytest.fixture
def rabbitmq():
    return AsyncMock()


@pytest.fixture
def service(repository, rabbitmq):
    return TaskService(
        repository=repository,
        rabbitmq=rabbitmq,
    )
