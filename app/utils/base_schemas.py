from pydantic import BaseModel


class SException(BaseModel):
    statusCode: int
    message: str


class ValidationErrorDetail(BaseModel):
    loc: list[str]
    msg: str
    type: str


class ErrorResponsePydantic(BaseModel):
    detail: list[ValidationErrorDetail]
