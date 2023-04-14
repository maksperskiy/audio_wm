from fastapi import status

from app.optimizer_api.exceptions.application import ApplicationException


class AccessDeniedException(ApplicationException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access denied"
