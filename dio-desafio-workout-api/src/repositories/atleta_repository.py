from sqlalchemy.orm import Session
from src.models.atleta import Atleta
from src.schemas.atleta import AtletaCreate

def listar(db: Session):
    return db.query(Atleta).all()

def criar(db: Session, atleta: AtletaCreate):
    novo = Atleta(**atleta.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo
