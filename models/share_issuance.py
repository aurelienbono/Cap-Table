# models/share_issuance.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey , String 
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship
import uuid

class ShareIssuance(Base):
    __tablename__ = "share_issuances"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    shareholder_id = Column(String(36), ForeignKey("shareholders.id"), nullable=False)
    number_of_shares = Column(Integer, nullable=False)
    price = Column(Float, nullable=True) 
    issued_date = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    shareholder = relationship("models.shareholder.Shareholder", back_populates="issuances")
    