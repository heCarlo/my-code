from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Base, User, Role
from schemas import UserCreate, RoleResponse
from use_cases.database import get_db, engine
from datetime import date
import random
import string

# Inicializando o FastAPI
app = FastAPI()

# Função para gerar uma senha aleatória
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Rota para obter o papel de um usuário pelo role_id
@app.get("/role/{role_id}", response_model=RoleResponse)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Rota para criar um usuário
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário com nome, e-mail e papel (role_id).
    Se a senha não for fornecida, uma senha aleatória será gerada.
    """
    # Verificar se o papel (role) existe no banco
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Gerar uma senha aleatória se não for fornecida
    password = user.password if user.password else generate_random_password()

    # Criar o novo usuário
    new_user = User(
        name=user.name,
        email=user.email,
        password=password,
        role_id=user.role_id,
        created_at=date.today()  # A data de criação será o dia atual
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
