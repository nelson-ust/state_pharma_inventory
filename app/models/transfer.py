from sqlalchemy import Column, Integer, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid
from datetime import datetime

class Transfer(Base):
    __tablename__ = "transfers"

    transfer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_facility_id = Column(UUID(as_uuid=True), ForeignKey("facilities.facility_id"), nullable=False)
    to_facility_id = Column(UUID(as_uuid=True), ForeignKey("facilities.facility_id"), nullable=False)
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.medication_id"), nullable=False)
    quantity_transferred = Column(Integer, nullable=False)
    transfer_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    from_facility = relationship("Facility", foreign_keys=[from_facility_id], back_populates="from_transfers")
    to_facility = relationship("Facility", foreign_keys=[to_facility_id], back_populates="to_transfers")
    medication = relationship("Medication", back_populates="transfers")
