from pydantic import BaseModel
from typing import Optional, List

class DepartmentBase(BaseModel):
    name: str
    budget: float = 0.0

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True

class BedBase(BaseModel):
    department_id: int
    bed_number: str
    status: str = "Available"

class BedResponse(BedBase):
    id: int

    class Config:
        from_attributes = True
