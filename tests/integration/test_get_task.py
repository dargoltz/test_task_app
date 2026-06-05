from fastapi import status


async def test_get_task_by_id(
    client,
    task_service_mock,
    task_response,
):
    task_service_mock.get_task.return_value = task_response

    response = await client.get(
        f"/api/v1/tasks/{task_response.id}"
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["id"] == str(task_response.id)
    assert body["name"] == task_response.name

    task_service_mock.get_task.assert_awaited_once()
