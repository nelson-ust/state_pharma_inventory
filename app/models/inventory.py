from sqlalchemy import Column, Integer, Date, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    facility_id = Column(UUID(as_uuid=True), ForeignKey("facilities.facility_id"), nullable=False)
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.medication_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    reorder_level = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)

    # Relationships
    facility = relationship("Facility", back_populates="inventory")
    medication = relationship("Medication", back_populates="inventory")
