from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import BaseModel

class Atleta(BaseModel):
    __tablename__ = "atletas"

    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    centro_treinamento_id = Column(Integer, ForeignKey("centros_treinamento.id"))

    categoria = relationship("Categoria", back_populates="atletas")
    centro_treinamento = relationship("CentroTreinamento", back_populates="atletas")
