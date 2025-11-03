# src/schemas/atleta.py
from typing import Annotated
from pydantic import BaseModel, Field, PositiveFloat
from src.schemas.schemas import BaseSchema, OutMixin

# Importar schemas de relacionamento que são necessários no body da requisição
# Assumindo que CategoriaIn e CentroTreinamentoIn existem
from src.schemas.categorias import CategoriaIn
from src.schemas.centros_treinamento import CentroTreinamentoIn


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=20)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=70.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]

class AtletaIn(Atleta):
    # CORREÇÃO: Adicionando os schemas aninhados para Categoria e CT.
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoIn, Field(description='Centro de Treinamento do atleta')]


class AtletaOut(AtletaIn, OutMixin):
    pass
