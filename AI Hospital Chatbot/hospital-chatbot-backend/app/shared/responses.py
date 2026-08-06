from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    """
    A standardized JSON response format for future modules to ensure 
    consistency across the Hospital Management System APIs.
    """
    status: str = "success"
    message: Optional[str] = None
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """
    Standardized error response.
    """
    status: str = "error"
    error: str
