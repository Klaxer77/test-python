from datetime import datetime

from pydantic import BaseModel, Field


class SCreateToDo(BaseModel):
    title: str = Field(max_length=100)


class SListTodo(BaseModel):
    id: int
    title: str
    is_completed: bool
    created_at: datetime


class SChangeToDo(BaseModel):
    title: str | None = Field(None, max_length=100)
    is_completed: bool | None = Field(default=None)
