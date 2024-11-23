from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., title="Nome do Usuário", max_length=100, example="Carlos Santos")
    email: EmailStr = Field(..., title="E-mail do Usuário", example="carlos.santos@example.com")
    password: Optional[str] = Field(None, title="Senha do Usuário", min_length=6, example="password123")
    role_id: int = Field(..., title="ID do Papel (Role) do Usuário", example=2)

    class Config:
        schema_extra = {
            "example": {
                "name": "Carlos Santos",
                "email": "carlos.santos@example.com",
                "password": "password123",
                "role_id": 2
            }
        }

class UserResponse(BaseModel):
    id: int = Field(..., title="ID do Usuário", example=1)
    name: str = Field(..., title="Nome do Usuário", example="Carlos Santos")
    email: EmailStr = Field(..., title="E-mail do Usuário", example="carlos.santos@example.com")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Carlos Santos",
                "email": "carlos.santos@example.com"
            }
        }
