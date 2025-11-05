from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.atleta import AtletaCreate, AtletaResponse
from src.api.controllers.atleta_controller import listar_atletas, criar_atleta

router = APIRouter()

@router.get("/", response_model=list[AtletaResponse])
def listar(db: Session = Depends(get_db)):
    return listar_atletas(db)

@router.post("/", response_model=AtletaResponse)
def criar(atleta: AtletaCreate, db: Session = Depends(get_db)):
    return criar_atleta(db, atleta)
