from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .models import BaseModel

class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    categoria: Mapped['CategoriaModel'] = relationship(
        "CategoriaModel", back_populates="atletas"
    )

    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey('centros_treinamento.pk_id'))
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(
        "CentroTreinamentoModel", back_populates="atletas"
    )
