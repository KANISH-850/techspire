from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    bed_number = Column(String)
    status = Column(String) # Occupied, Available, Maintenance

    department = relationship("Department", back_populates="beds")
