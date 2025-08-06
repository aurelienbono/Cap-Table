# models/shareholder.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

import uuid

class Shareholder(Base):
    __tablename__ = "shareholders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False) 
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="shareholder_profile")
    issuances = relationship("models.share_issuance.ShareIssuance", back_populates="shareholder", cascade="all, delete-orphan") 