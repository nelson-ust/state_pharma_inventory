from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

class Medication(Base):
    __tablename__ = "medications"

    medication_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medication_name = Column(String, nullable=False)
    dosage_form = Column(String, nullable=False)
    strength = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)

    # Relationships
    inventory = relationship("Inventory", back_populates="medication")
    requisitions = relationship("Requisition", back_populates="medication")
    transfers = relationship("Transfer", back_populates="medication")
