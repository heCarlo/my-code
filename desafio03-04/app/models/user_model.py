from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=True)

    role = relationship("Role", back_populates="users")
    claims = relationship("Claim", secondary="user_claims", back_populates="users")
