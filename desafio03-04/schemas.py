from pydantic import BaseModel, EmailStr
from typing import Optional

# Modelo Pydantic para criação de usuário
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role_id: int
    password: Optional[str] = None  # A senha é opcional

    class Config:
        orm_mode = True  # Alterado para a nova chave no Pydantic V2


# Modelo Pydantic para resposta de papel (role)
class RoleResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode = True  # Alterado para a nova chave no Pydantic V2
