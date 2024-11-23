from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, index=True)
    active = Column(Boolean, nullable=False, default=True)

    users = relationship("User", secondary="user_claims", back_populates="claims")
