import pytest

from app.item.service import TodoService


class TestIntegrationItem:

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "title",
        [
            ("Задача27"),
            ("Задача28"),
            ("Задача29"),
        ],
    )
    async def test_item_create(self, title: str):
        new_todo = await TodoService.create(title=title)
        assert new_todo

        find_new_todo = await TodoService.find_one_or_none(new_todo["id"])
        assert find_new_todo

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "todo_id",
        [
            (4),
            (5),
        ],
    )
    async def test_item_delete(self, todo_id: int):
        deleted_todo = await TodoService.delete(todo_id=todo_id)
        assert deleted_todo

        find_new_todo = await TodoService.find_one_or_none(deleted_todo["id"])
        assert find_new_todo is None
