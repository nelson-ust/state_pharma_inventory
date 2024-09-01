from sqlalchemy import Column, Integer, ForeignKey, UUID, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid
from datetime import datetime

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    purchase_order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.vendor_id"), nullable=False)
    requisition_id = Column(UUID(as_uuid=True), ForeignKey("requisition.requisition_id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery_date = Column(DateTime, nullable=False)

    # Relationships
    vendor = relationship("Vendor", back_populates="purchase_orders")
    requisition = relationship("Requisition", back_populates="purchase_orders")
