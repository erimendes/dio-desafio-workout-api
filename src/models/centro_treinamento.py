from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    atletas: Mapped[list['AtletaModel']] = relationship(
        "AtletaModel", 
        back_populates='centro_treinamento'
    )
