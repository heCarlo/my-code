from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class UserClaim(Base):
    __tablename__ = "user_claims"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), primary_key=True)
