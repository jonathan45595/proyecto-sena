from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ParcelaBase(BaseModel):
    cliente_id: int
    nombre: str = Field(min_length=2, max_length=120)
    cultivo: str = Field(min_length=2, max_length=80)
    hectareas: float = Field(gt=0)
    ubicacion: str | None = Field(default=None, max_length=255)
    notas: str | None = None


class ParcelaCreate(ParcelaBase):
    pass


class ParcelaRead(ParcelaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
