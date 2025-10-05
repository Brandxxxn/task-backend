from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Standard API response model"""
    success: bool
    message: str
    data: Optional[T] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation successful",
                "data": {}
            }
        }


def success_response(message: str = "Success", data: Any = None) -> dict:
    """Helper function to create success responses"""
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str = "Error", data: Any = None) -> dict:
    """Helper function to create error responses"""
    return {
        "success": False,
        "message": message,
        "data": data
    }
