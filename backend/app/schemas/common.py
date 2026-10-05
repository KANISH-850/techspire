from pydantic import BaseModel
from typing import Optional, Any

class MessageResponse(BaseModel):
    message: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str = "healthy"
    app: str
    version: str
