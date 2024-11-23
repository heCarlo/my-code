from pydantic import BaseModel, Field
from typing import Optional

class RoleResponse(BaseModel):
    id: int = Field(..., title="ID do Papel", example=1)
    description: str = Field(..., title="Nome do Papel", example="Administrador")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "description": "Administrador"
            }
        }
