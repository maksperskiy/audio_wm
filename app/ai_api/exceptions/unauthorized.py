from fastapi import status

from app.ai_api.exceptions.application import ApplicationException


class UnauthorizedException(ApplicationException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"
