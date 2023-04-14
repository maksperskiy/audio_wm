from fastapi import status

from app.optimizer_api.exceptions.application import ApplicationException


class ValidationException(ApplicationException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Value is not valid type"
