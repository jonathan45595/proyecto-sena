from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import citas, clientes, parcelas


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FlyMetrics API",
    description="API de agendamiento de citas para servicios agrícolas con drones.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router, prefix="/api")
app.include_router(parcelas.router, prefix="/api")
app.include_router(citas.router, prefix="/api")


@app.get("/")
def root():
    return {
        "nombre": "FlyMetrics API",
        "mensaje": "Sistema de agendamiento de citas con drones",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
