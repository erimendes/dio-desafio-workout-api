from sqlalchemy.orm import Session
from src.repositories import atleta_repository
from src.schemas.atleta import AtletaCreate

def listar_atletas(db: Session):
    return atleta_repository.listar(db)

def criar_atleta(db: Session, atleta: AtletaCreate):
    return atleta_repository.criar(db, atleta)
