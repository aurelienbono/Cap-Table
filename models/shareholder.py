# models/shareholder.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Shareholder(Base):
    __tablename__ = "shareholders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="shareholder_profile")
    # issuances = relationship("ShareIssuance", back_populates="shareholder", cascade="all, delete-orphan")