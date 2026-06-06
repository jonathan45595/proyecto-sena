from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.cita import EstadoCita, TipoServicio


class CitaBase(BaseModel):
    cliente_id: int
    parcela_id: int
    fecha_programada: datetime
    tipo_servicio: TipoServicio = TipoServicio.fumigacion
    estado: EstadoCita = EstadoCita.pendiente
    operador: str | None = Field(default=None, max_length=120)
    notas: str | None = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    fecha_programada: datetime | None = None
    tipo_servicio: TipoServicio | None = None
    estado: EstadoCita | None = None
    operador: str | None = Field(default=None, max_length=120)
    notas: str | None = None


class CitaRead(CitaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
