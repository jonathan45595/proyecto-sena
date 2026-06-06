from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import Cliente
from app.models.parcela import Parcela
from app.schemas.parcela import ParcelaCreate, ParcelaRead

router = APIRouter(prefix="/parcelas", tags=["Parcelas"])


@router.get("/", response_model=list[ParcelaRead])
def listar_parcelas(db: Session = Depends(get_db)):
    return db.query(Parcela).order_by(Parcela.nombre).all()


@router.post("/", response_model=ParcelaRead, status_code=status.HTTP_201_CREATED)
def crear_parcela(payload: ParcelaCreate, db: Session = Depends(get_db)):
    cliente = db.get(Cliente, payload.cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )

    parcela = Parcela(**payload.model_dump())
    db.add(parcela)
    db.commit()
    db.refresh(parcela)
    return parcela
