from typing import Annotated
from pydantic import UUID4, Field, BaseModel
from src.schemas.schemas import BaseSchema, OutMixin

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do Centro de Treinamento', example='Rua X, 100', max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do proprietário do CT', example='Marcos', max_length=30)]

class CentroTreinamento(BaseModel):
    # Usado para receber o Centro de Treinamento como um objeto aninhado
    # na requisição do Atleta. Para evitar complexidade, podemos receber apenas o nome.
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento para vincular o atleta', example='CT King', max_length=20)]

class CentroTreinamentoAtleta(BaseSchema):
    # Schema simplificado usado dentro do AtletaOut
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='CT King', max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn, OutMixin):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]
    # Schema completo de saída
    pass
