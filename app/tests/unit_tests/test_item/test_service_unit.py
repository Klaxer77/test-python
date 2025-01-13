import pytest

from app.item.schemas import SChangeToDo
from app.item.service import TodoService


class TestUnitItems:

    @pytest.mark.asyncio
    async def test_item_find_all(self):
        items = await TodoService.find_all()
        assert items

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "id, if_existing, title",
        [
            (1, True, "Задача1"),
            (2, True, "Задача2"),
            (3, True, "Задача3"),
            (500, False, "..."),
        ],
    )
    async def test_item_find_one_or_none(self, id: int, if_existing: bool, title: str):
        items = await TodoService.find_one_or_none(todo_id=id)
        if if_existing:
            assert items
            assert items["title"] == title
        else:
            assert items is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("title", [("Задача5"), ("Задача6")])
    async def test_item_create(self, title: str):
        new_item = await TodoService.create(title=title)
        assert new_item

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "todo_id,title,is_completed",
        [
            (1, "Задача34", None),
            (2, "Задача54", None),
            (3, None, True),
            (2, None, True),
            (1, "Задача80", True),
        ],
    )
    async def test_item_change(
        self, todo_id: int, title: str | None, is_completed: bool | None
    ):
        if title:
            user_data = SChangeToDo(title=title)
        if is_completed:
            user_data = SChangeToDo(is_completed=is_completed)
        if title and is_completed:
            user_data = SChangeToDo(is_completed=is_completed, title=title)
        modifid_item = await TodoService.change_todo(
            todo_id=todo_id, user_data=user_data
        )

        assert modifid_item

    @pytest.mark.asyncio
    @pytest.mark.parametrize("todo_id", [(1), (2), (3)])
    async def test_item_delete(self, todo_id: int):
        deleted_item = await TodoService.delete(todo_id=todo_id)
        assert deleted_item
