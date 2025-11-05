from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Não é estritamente necessário importar AtletaModel aqui se for usado apenas como string
# from .atleta import AtletaModel 
from .base import BaseModel

class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)
    
    # create_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    atletas: Mapped[list['AtletaModel']] = relationship(
        "AtletaModel", # É recomendado usar a string, mesmo com a importação
        back_populates='centro_treinamento'
    )
