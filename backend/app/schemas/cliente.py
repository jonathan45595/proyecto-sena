from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    email: EmailStr
    telefono: str | None = Field(default=None, max_length=30)


class ClienteCreate(ClienteBase):
    pass


class ClienteRead(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
