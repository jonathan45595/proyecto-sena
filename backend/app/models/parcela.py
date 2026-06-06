from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Parcela(Base):
    __tablename__ = "parcelas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    cultivo: Mapped[str] = mapped_column(String(80), nullable=False)
    hectareas: Mapped[float] = mapped_column(Float, nullable=False)
    ubicacion: Mapped[str | None] = mapped_column(String(255))
    notas: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    cliente: Mapped["Cliente"] = relationship(back_populates="parcelas")
    citas: Mapped[list["Cita"]] = relationship(back_populates="parcela")
