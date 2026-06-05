from fastapi import status


async def test_get_tasks(
    client,
    task_service_mock,
    page_response,
):
    task_service_mock.get_tasks.return_value = page_response

    response = await client.get("/api/v1/tasks/")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["page"] == 1
    assert body["limit"] == 100
    assert body["total"] == 1
    assert len(body["items"]) == 1

    task_service_mock.get_tasks.assert_awaited_once()


async def test_get_tasks_with_filters(
    client,
    task_service_mock,
    page_response,
):
    task_service_mock.get_tasks.return_value = page_response

    response = await client.get(
        "/api/v1/tasks/?status=pending&priority=low"
    )

    assert response.status_code == status.HTTP_200_OK

    task_service_mock.get_tasks.assert_awaited_once()
