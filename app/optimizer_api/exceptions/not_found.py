from fastapi import status

from app.optimizer_api.exceptions.application import ApplicationException


class NotFoundException(ApplicationException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"
