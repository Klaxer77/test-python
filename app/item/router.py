from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions.item.exceptions import ExcItemNotFound
from app.item.schemas import SChangeToDo, SCreateToDo, SListTodo
from app.item.service import TodoService
from app.utils.base_schemas import SException
from app.utils.custom_coder_cache import ORJsonCoder

router = APIRouter(prefix="/todo", tags=["Item"])


@router.post("", status_code=201, responses={201: {"model": SListTodo}})
async def create(user_data: SCreateToDo) -> SListTodo:
    """
    **Создать задачу**

    **Args**

    `title` - заголовок для задачи _max_length 100_
    """
    todo = await TodoService.create(title=user_data.title)
    return todo


@router.get("", responses={200: {"model": list[SListTodo]}})
@cache(expire=30, coder=ORJsonCoder)  # кэш на 30 секунд
async def find_all() -> list[SListTodo]:
    """
    **Посмотреть все задачи**
    """
    todos = await TodoService.find_all()
    return todos


@router.get("/{id}", responses={404: {"model": SException}, 200: {"model": SListTodo}})
@cache(expire=30, coder=ORJsonCoder)  # кэш на 30 секунд
async def find_detail(id: int) -> SListTodo:
    """
    **Посмотреть конкретную задачу**

    **Args**

    `id` - идентификатор просматриваемой задачи
    """
    todo = await TodoService.find_one_or_none(todo_id=id)
    if not todo:
        raise ExcItemNotFound
    return todo


@router.put("/{id}", status_code=200, responses={404: {"model": SException}})
async def change(id: int, user_data: SChangeToDo) -> SListTodo:
    """
    **Изменить конкретную задачу**

    **Args**

    `id` - идентификатор изменяемой задачи

    `title` - заголовок для задачи _max_length 100_

    `is_completed` - _true_ - завершенная | _false_ - не завершенная
    """
    existed_todo = await TodoService.find_one_or_none(todo_id=id)

    if not existed_todo:
        raise ExcItemNotFound

    modified_todo = await TodoService.change_todo(todo_id=id, user_data=user_data)
    return modified_todo


@router.delete("/{id}", status_code=200, responses={404: {"model": SException}})
async def delete(id: int) -> SListTodo:
    """
    **Удалить задачу**

    **Args**

    `id` - идентификатор удаляемой задачи
    """
    existed_todo = await TodoService.find_one_or_none(todo_id=id)

    if not existed_todo:
        raise ExcItemNotFound

    deleted_todo = await TodoService.delete(todo_id=id)
    return deleted_todo
