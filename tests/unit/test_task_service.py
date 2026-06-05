import uuid

import pytest


@pytest.mark.asyncio
async def test_create_task(
    service,
    repository,
    rabbitmq,
    task_request,
    task,
):
    task.id = uuid.uuid4()

    repository.create.return_value = task

    result = await service.create_task(task_request)

    repository.create.assert_awaited_once()
    repository.update_status.assert_awaited_once_with(task)

    rabbitmq.send_message.assert_awaited_once_with(
        {"task_id": str(task.id)},
        task.priority,
    )

    assert result.id == task.id


@pytest.mark.asyncio
async def test_get_task_status(
    service,
    repository,
    task,
):
    repository.get_by_id.return_value = task

    result = await service.get_task_status(task.id)

    repository.get_by_id.assert_awaited_once_with(task.id)

    assert result == task.status.value


@pytest.mark.asyncio
async def test_cancel_task(
    service,
    repository,
    task,
):
    repository.get_by_id.return_value = task

    await service.cancel_task(task.id)

    repository.get_by_id.assert_awaited_once_with(task.id)
    repository.update_status.assert_awaited_once_with(task)
