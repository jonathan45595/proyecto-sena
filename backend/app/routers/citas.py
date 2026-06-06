from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cita import Cita
from app.models.cliente import Cliente
from app.models.parcela import Parcela
from app.schemas.cita import CitaCreate, CitaRead, CitaUpdate

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.get("/", response_model=list[CitaRead])
def listar_citas(db: Session = Depends(get_db)):
    return (
        db.query(Cita)
        .order_by(Cita.fecha_programada.desc())
        .all()
    )


@router.post("/", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(payload: CitaCreate, db: Session = Depends(get_db)):
    cliente = db.get(Cliente, payload.cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    parcela = db.get(Parcela, payload.parcela_id)
    if not parcela:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcela no encontrada.",
        )

    if parcela.cliente_id != payload.cliente_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La parcela no pertenece al cliente indicado.",
        )

    cita = Cita(**payload.model_dump())
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


@router.patch("/{cita_id}", response_model=CitaRead)
def actualizar_cita(cita_id: int, payload: CitaUpdate, db: Session = Depends(get_db)):
    cita = db.get(Cita, cita_id)
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada.",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cita, field, value)

    db.commit()
    db.refresh(cita)
    return cita
