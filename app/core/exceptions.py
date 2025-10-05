from fastapi import HTTPException, status
from typing import Any, Optional


class APIException(HTTPException):
    """Base exception class for API errors"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        success: bool = False,
        data: Optional[Any] = None
    ):
        self.status_code = status_code
        self.message = message
        self.success = success
        self.data = data
        super().__init__(status_code=status_code, detail={
            "success": success,
            "message": message,
            "data": data
        })


class BadRequestException(APIException):
    def __init__(self, message: str = "Bad Request", data: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            success=False,
            data=data
        )


class UnauthorizedException(APIException):
    def __init__(self, message: str = "Unauthorized", data: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            success=False,
            data=data
        )


class ForbiddenException(APIException):
    def __init__(self, message: str = "Forbidden", data: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            success=False,
            data=data
        )


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found", data: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            success=False,
            data=data
        )


class ConflictException(APIException):
    def __init__(self, message: str = "Conflict", data: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            success=False,
            data=data
        )


class InternalServerException(APIException):
    def __init__(self, message: str = "Internal Server Error", data: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            success=False,
            data=data
        )
