from sqlalchemy.orm import Session
from ..models.claim_model import Claim

class ClaimRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_claims(self):
        return self.db.query(Claim).all()
