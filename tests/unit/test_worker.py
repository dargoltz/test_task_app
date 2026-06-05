import json
import uuid
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from src.domain.exceptions import EntityNotFoundError, TaskExecutionError
from src.persistence.orm_models import TaskORM
from src.worker.task_processing import process_task


@pytest.mark.asyncio
async def test_process_task_success():
    task_id = uuid.uuid4()

    task = MagicMock()

    repository = AsyncMock()
    repository.get_by_id.return_value = task

    session = AsyncMock()

    with (
        patch("src.worker.task_processing.get_db_session") as get_db_session,
        patch("src.worker.task_processing.TaskRepository", return_value=repository),
        patch("src.worker.task_processing.execute_task", return_value="success"),
        patch("src.worker.task_processing.TaskStatusManager") as status_manager,
    ):
        get_db_session.return_value.__aenter__.return_value = session
        get_db_session.return_value.__aexit__.return_value = None

        await process_task(task_id)

        repository.get_by_id.assert_awaited_once_with(
            task_id,
            for_update=True,
        )

        status_manager.start.assert_called_once_with(task=task)

        status_manager.complete.assert_called_once_with(
            task=task,
            result="success",
        )

        assert repository.update_status.await_count == 2


@pytest.mark.asyncio
async def test_process_task_not_found():
    task_id = uuid.uuid4()

    repository = AsyncMock()
    repository.get_by_id.side_effect = EntityNotFoundError(TaskORM, task_id)

    session = AsyncMock()

    with (
        patch("src.worker.task_processing.get_db_session") as get_db_session,
        patch("src.worker.task_processing.TaskRepository", return_value=repository),
    ):
        get_db_session.return_value.__aenter__.return_value = session
        get_db_session.return_value.__aexit__.return_value = None

        await process_task(task_id)

        repository.update_status.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_task_execution_error():
    task_id = uuid.uuid4()

    task = MagicMock()

    repository = AsyncMock()
    repository.get_by_id.return_value = task

    session = AsyncMock()

    with (
        patch("src.worker.task_processing.get_db_session") as get_db_session,
        patch("src.worker.task_processing.TaskRepository", return_value=repository),
        patch(
            "src.worker.task_processing.execute_task",
            side_effect=TaskExecutionError(task_id),
        ),
        patch("src.worker.task_processing.TaskStatusManager") as status_manager,
    ):
        get_db_session.return_value.__aenter__.return_value = session
        get_db_session.return_value.__aexit__.return_value = None

        await process_task(task_id)

        status_manager.fail.assert_called_once()

        repository.update_status.assert_awaited()


@pytest.mark.asyncio
async def test_process_task_unexpected_error():
    task_id = uuid.uuid4()

    task = MagicMock()

    repository = AsyncMock()
    repository.get_by_id.return_value = task

    session = AsyncMock()

    with (
        patch("src.worker.task_processing.get_db_session") as get_db_session,
        patch("src.worker.task_processing.TaskRepository", return_value=repository),
        patch(
            "src.worker.task_processing.execute_task",
            side_effect=RuntimeError("boom"),
        ),
        patch("src.worker.task_processing.TaskStatusManager") as status_manager,
    ):
        get_db_session.return_value.__aenter__.return_value = session
        get_db_session.return_value.__aexit__.return_value = None

        await process_task(task_id)

        status_manager.fail.assert_called_once()

        repository.update_status.assert_awaited()
