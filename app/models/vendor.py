from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_name = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
