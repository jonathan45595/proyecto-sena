from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import RegisterRequest
from app.utils.security import hash_password 

router = APIRouter(tags=["Auth"])


@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):
    usuario_existente = (
        db.query(Usuario)
        .filter(
            Usuario.email == payload.email
        )
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya está registrado."
        )

    nuevo_usuario = Usuario(
        nombre=payload.nombre,
        apellido=payload.apellido,
        email=payload.email,
        telefono=payload.telefono,
        password_hash=hash_password(
            payload.password
        ),
        rol="cliente",
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "message": "Usuario registrado correctamente"
    }