import pytest
from httpx import AsyncClient
from pydantic import BaseModel

from app.item.schemas import SListTodo
from app.utils.base_schemas import ErrorResponsePydantic, SException


class TestApiItems:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id, status_code, response_model",
        [
            (1, 200, SListTodo),
            (2, 200, SListTodo),
            (3, 200, SListTodo),
            (500, 404, SException),
            ("adawd", 422, ErrorResponsePydantic),
        ],
    )
    async def test_api_items_find_detail(
        self, id: int, status_code: int, response_model: BaseModel, ac: AsyncClient
    ):
        response = await ac.get(f"http://localhost:8000/api/todo/{id}")
        todo = response.json()
        assert todo

        assert response.status_code == status_code

        assert response_model.model_validate(todo)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "title, status_code, response_model",
        [
            ("Задача67", 201, SListTodo),
            ("Задача60", 201, SListTodo),
            ("Задача34", 201, SListTodo),
            (11111, 422, ErrorResponsePydantic),
        ],
    )
    async def test_api_items_create_and_find_item(
        self, title: str, status_code: int, response_model: BaseModel, ac: AsyncClient
    ):
        response = await ac.post(
            f"http://localhost:8000/api/todo", json={"title": title}
        )
        new_todo = response.json()
        assert new_todo

        assert response.status_code == status_code

        assert response_model.model_validate(new_todo)

        if str(status_code).startswith("2"):
            response_new_todo = await ac.get(
                f"http://localhost:8000/api/todo/{new_todo['id']}"
            )
            find_new_todo = response_new_todo.json()
            assert find_new_todo

    @pytest.mark.asyncio
    async def test_api_items_find_all(
        self,
        ac: AsyncClient,
        status_code: int = 200,
        response_model: BaseModel = SListTodo,
    ):
        response = await ac.get("http://localhost:8000/api/todo")
        todos = response.json()
        assert todos
        assert isinstance(todos, list)

        assert response.status_code == status_code
        for todo in todos:
            assert response_model.model_validate(todo)
