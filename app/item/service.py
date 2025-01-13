from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.item.models import TodoItem
from app.item.schemas import SChangeToDo
from app.logger import logger


class TodoService:

    @staticmethod
    async def create(title: str):
        try:
            async with async_session_maker() as session:
                query = (
                    insert(TodoItem)
                    .values(title=title)
                    .returning(TodoItem.__table__.columns)
                )
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add todo"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add todo"
            extra = {"title": title}
            logger.error(msg, extra=extra, exc_info=True)

    @staticmethod
    async def find_all():
        try:
            async with async_session_maker() as session:
                query = select(TodoItem.__table__.columns)
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot find todos"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot find todos"
            logger.error(msg, exc_info=True)

    @staticmethod
    async def find_one_or_none(todo_id: int):
        try:
            async with async_session_maker() as session:
                query = select(TodoItem.__table__.columns).filter_by(id=todo_id)
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot find one todo"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot find one todo"
            extra = {"todo_id": todo_id}
            logger.error(msg, extra=extra, exc_info=True)

    @staticmethod
    async def change_todo(todo_id: int, user_data: SChangeToDo):
        try:
            async with async_session_maker() as session:
                user_dict = user_data.model_dump(exclude_unset=True)

                query = (
                    update(TodoItem)
                    .filter_by(id=todo_id)
                    .values(**user_dict)
                    .returning(TodoItem.__table__.columns)
                )
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot change todo"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot change todo"
            extra = {
                "todo_id": todo_id,
                "title": user_data.title,
                "is_completed": user_data.is_completed,
            }
            logger.error(msg, extra=extra, exc_info=True)

    @staticmethod
    async def delete(todo_id: int):
        try:
            async with async_session_maker() as session:
                query = (
                    delete(TodoItem)
                    .filter_by(id=todo_id)
                    .returning(TodoItem.__table__.columns)
                )
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot delete todo"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot delete todo"
            extra = {"todo_id": todo_id}
            logger.error(msg, extra=extra, exc_info=True)
