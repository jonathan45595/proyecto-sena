from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteRead

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[ClienteRead])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).order_by(Cliente.nombre).all()


@router.post("/", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def crear_cliente(payload: ClienteCreate, db: Session = Depends(get_db)):
    existe = db.query(Cliente).filter(Cliente.email == payload.email).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un cliente con ese correo.",
        )

    cliente = Cliente(**payload.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente
