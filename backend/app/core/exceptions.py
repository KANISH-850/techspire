from fastapi import Request
from fastapi.responses import JSONResponse

class HMSException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

async def hms_exception_handler(request: Request, exc: HMSException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.message}
    )
