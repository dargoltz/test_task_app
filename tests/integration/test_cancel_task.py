from fastapi import status


async def test_cancel_task(
    client,
    task_service_mock,
    task_id,
):
    task_service_mock.cancel_task.return_value = None

    response = await client.delete(
        f"/api/v1/tasks/{task_id}"
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["message"] == f"Task {task_id} cancelled"

    task_service_mock.cancel_task.assert_awaited_once()
