from fastapi import Request, status
from fastapi.responses import JSONResponse


class HospitalChatbotException(Exception):
    """
    Base exception class for the Chatbot application.
    """
    def __init__(
        self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.message = message
        self.status_code = status_code


class NotFoundException(HospitalChatbotException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


async def hospital_chatbot_exception_handler(
    request: Request, exc: HospitalChatbotException
):
    """
    FastAPI exception handler for custom HospitalChatbotException.
    """
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.message, "status": "error"}
    )
