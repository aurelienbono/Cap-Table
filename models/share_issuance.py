# models/share_issuance.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class ShareIssuance(Base):
    __tablename__ = "share_issuances"

    id = Column(Integer, primary_key=True, index=True)
    shareholder_id = Column(Integer, ForeignKey("shareholders.id"), nullable=False)
    number_of_shares = Column(Integer, nullable=False)
    price = Column(Float, nullable=True) 
    issued_date = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    shareholder = relationship("Shareholder", back_populates="issuances")