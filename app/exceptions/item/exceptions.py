from fastapi import status

from app.exceptions.base import BaseHTTPException


class ExcItemNotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Задачи не существует"
