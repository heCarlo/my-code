from sqlalchemy.orm import Session
from ..models.user_model import User
from ..models.claim_model import Claim
from ..models.role_model import Role


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(db, user):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_all_users(self):
        return self.db.query(User).all()
    
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_users_with_role_and_claims(self):
        return (
            self.db.query(User, Role, Claim)
            .join(Role, User.role_id == Role.id)
            .join(User.claims)
            .join(Claim)
            .all()
        )
