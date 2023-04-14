from typing import Any

from fastapi import HTTPException, status


class ApplicationException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

    def __init__(self, status_code: int = None, detail: Any = None):
        super(ApplicationException, self).__init__(
            status_code=status_code or self.status_code, detail=detail or self.detail
        )
