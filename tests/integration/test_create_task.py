from fastapi import status


async def test_create_task(
    client,
    task_service_mock,
    task_response,
):
    task_service_mock.create_task.return_value = task_response

    payload = {
        "name":        "Test task",
        "description": "Test description",
        "priority":    "low",
    }

    response = await client.post("/api/v1/tasks/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["id"] == str(task_response.id)
    assert body["name"] == payload["name"]
    assert body["description"] == payload["description"]
    assert body["priority"] == "low"

    task_service_mock.create_task.assert_awaited_once()
