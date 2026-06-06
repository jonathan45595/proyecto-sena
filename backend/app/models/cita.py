import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EstadoCita(str, enum.Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    en_proceso = "en_proceso"
    completada = "completada"
    cancelada = "cancelada"


class TipoServicio(str, enum.Enum):
    fumigacion = "fumigacion"
    monitoreo = "monitoreo"
    siembra = "siembra"
    mapeo = "mapeo"


class Cita(Base):
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    parcela_id: Mapped[int] = mapped_column(ForeignKey("parcelas.id"), nullable=False)
    fecha_programada: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tipo_servicio: Mapped[TipoServicio] = mapped_column(
        Enum(TipoServicio), nullable=False, default=TipoServicio.fumigacion
    )
    estado: Mapped[EstadoCita] = mapped_column(
        Enum(EstadoCita), nullable=False, default=EstadoCita.pendiente
    )
    operador: Mapped[str | None] = mapped_column(String(120))
    notas: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    cliente: Mapped["Cliente"] = relationship(back_populates="citas")
    parcela: Mapped["Parcela"] = relationship(back_populates="citas")
