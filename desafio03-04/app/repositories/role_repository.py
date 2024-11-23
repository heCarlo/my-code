from ..models.role_model import Role
from sqlalchemy.orm import Session

class RoleRepository:
    @staticmethod
    def get_role_by_id(db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()
