from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.user_service import UserService
from ..services.role_service import RoleService
from ..database.database import get_db
from ..schemas.user_schema import UserCreate, UserResponse
from ..schemas.role_schema import RoleResponse

router = APIRouter()

@router.get("/role/{role_id}", response_model=RoleResponse, summary="Obter role por ID", description="Obtém um papel (role) específico a partir do ID fornecido.")
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role = RoleService.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/users/", response_model=UserResponse, summary="Criar usuário", description="Cria um novo usuário no sistema.")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return UserService.create_user(db, user)
