from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from .base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, index=True)

    users = relationship("User", back_populates="role")
