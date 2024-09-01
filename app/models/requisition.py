# app/models/requisition.py

from sqlalchemy import Column, Integer, Enum, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid
from datetime import datetime
from enum import Enum as PyEnum

class RequisitionStatus(PyEnum):  # Use Python's Enum
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Requisition(Base):
    __tablename__ = "requisition"

    requisition_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    facility_id = Column(UUID(as_uuid=True), ForeignKey("facilities.facility_id"), nullable=False)
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.medication_id"), nullable=False)
    quantity_requested = Column(Integer, nullable=False)
    status = Column(Enum(RequisitionStatus), default=RequisitionStatus.pending, nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="requisitions")
    medication = relationship("Medication", back_populates="requisitions")
    purchase_orders = relationship("PurchaseOrder", back_populates="requisition")
