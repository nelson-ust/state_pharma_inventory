# app/models/user.py

from sqlalchemy import Column, String, Enum, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid
from enum import Enum as PyEnum

class UserRole(PyEnum):  # Use Python's Enum
    admin = "admin"
    facility_staff = "facility_staff"
    state_official = "state_official"

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    facility_id = Column(UUID(as_uuid=True), ForeignKey("facilities.facility_id"), nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)  # Pass the Enum members

    # Relationships
    facility = relationship("Facility", back_populates="users")
