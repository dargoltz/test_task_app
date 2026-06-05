from datetime import datetime

import pytest
from freezegun import freeze_time

from src.domain.exceptions import TaskStatusError
from src.domain.value_objects import TaskStatus
from src.service import TaskStatusManager


def test_set_pending_from_new(task):
    task.status = TaskStatus.NEW

    TaskStatusManager.set_pending(task)

    assert task.status == TaskStatus.PENDING


def test_set_pending_from_failed(task):
    task.status = TaskStatus.FAILED

    TaskStatusManager.set_pending(task)

    assert task.status == TaskStatus.PENDING


def test_set_pending_invalid(task):
    task.status = TaskStatus.IN_PROGRESS

    with pytest.raises(TaskStatusError):
        TaskStatusManager.set_pending(task)


@freeze_time("2026-01-01 12:00:00")
def test_start_success(task):
    task.status = TaskStatus.PENDING

    TaskStatusManager.start(task)

    assert task.status == TaskStatus.IN_PROGRESS
    assert task.started_at == datetime(2026, 1, 1, 12, 0, 0)


def test_start_invalid(task):
    task.status = TaskStatus.NEW

    with pytest.raises(TaskStatusError):
        TaskStatusManager.start(task)


@freeze_time("2026-01-01 12:00:00")
def test_complete_success(task):
    task.status = TaskStatus.IN_PROGRESS

    TaskStatusManager.complete(task, result="ok")

    assert task.status == TaskStatus.COMPLETED
    assert task.result == "ok"
    assert task.finished_at == datetime(2026, 1, 1, 12, 0, 0)


def test_complete_invalid(task):
    task.status = TaskStatus.PENDING

    with pytest.raises(TaskStatusError):
        TaskStatusManager.complete(task, result="ok")


@freeze_time("2026-01-01 12:00:00")
def test_fail_always_allowed(task):
    TaskStatusManager.fail(task, error="boom")

    assert task.status == TaskStatus.FAILED
    assert task.error == "boom"
    assert task.finished_at == datetime(2026, 1, 1, 12, 0, 0)


def test_cancel_success_from_new(task):
    task.status = TaskStatus.NEW

    TaskStatusManager.cancel(task)

    assert task.status == TaskStatus.CANCELLED


def test_cancel_success_from_pending(task):
    task.status = TaskStatus.PENDING

    TaskStatusManager.cancel(task)

    assert task.status == TaskStatus.CANCELLED


def test_cancel_invalid(task):
    task.status = TaskStatus.IN_PROGRESS

    with pytest.raises(TaskStatusError):
        TaskStatusManager.cancel(task)