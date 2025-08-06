# models/audit_event.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    action = Column(String, nullable=False)  
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    details = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())