from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    apellido: str = Field(min_length=2, max_length=80)
    email: EmailStr
    telefono: str | None = Field(default=None, max_length=20)
    password: str = Field(min_length=6, max_length=128)
    rol: RolUsuario = RolUsuario.cliente


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str | None = None
    rol: RolUsuario
    activo: bool
    creado_en: datetime
    actualizado_en: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str | None = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
