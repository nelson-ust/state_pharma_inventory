# app/models/facility.py

from sqlalchemy import Column, String, Enum, UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid
from enum import Enum as PyEnum

class FacilityType(PyEnum):  # Use Python's Enum
    hospital = "hospital"
    clinic = "clinic"
    megastore = "megastore"

class Facility(Base):
    __tablename__ = "facilities"

    facility_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    facility_name = Column(String, nullable=False)
    facility_type = Column(Enum(FacilityType), nullable=False)  # Pass the Enum members
    address = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)

    # Relationships
    inventory = relationship("Inventory", back_populates="facility")
    requisitions = relationship("Requisition", back_populates="facility")
    from_transfers = relationship("Transfer", foreign_keys="[Transfer.from_facility_id]", back_populates="from_facility")
    to_transfers = relationship("Transfer", foreign_keys="[Transfer.to_facility_id]", back_populates="to_facility")
    users = relationship("User", back_populates="facility")
