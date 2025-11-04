# src/schemas/atleta.py

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field, PositiveFloat
from src.schemas.schemas import BaseSchema, OutMixin
from src.schemas.categorias import CategoriaIn
from src.schemas.centros_treinamento import CentroTreinamentoIn

# Schemas para entrada (usados no POST)
class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=20)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=70.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]


class AtletaIn(Atleta):
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoIn, Field(description='Centro de Treinamento do atleta')]


# Schemas para saída (usados no retorno da API)
class CategoriaOut(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class CentroTreinamentoOut(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class AtletaOut(OutMixin):
    pk_id: int
    nome: str
    cpf: str
    idade: int
    peso: float
    altura: float
    sexo: str
    created_at: datetime

    categoria: CategoriaOut
    centro_treinamento: CentroTreinamentoOut

    class Config:
        from_attributes = True  # Necessário para funcionar com SQLAlchemy ORM

class AtletaUpdate(BaseSchema):
    nome: Optional[str] = Field(default=None, description='Nome do atleta', example='João', max_length=50)
    cpf: Optional[str] = Field(default=None, description='CPF do atleta', example='12345678900', max_length=11)
    idade: Optional[int] = Field(default=None, description='Idade do atleta', example=20)
    peso: Optional[PositiveFloat] = Field(default=None, description='Peso do atleta', example=70.5)
    altura: Optional[PositiveFloat] = Field(default=None, description='Altura do atleta', example=1.70)
    sexo: Optional[str] = Field(default=None, description='Sexo do atleta', example='M', max_length=1)