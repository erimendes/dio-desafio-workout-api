from typing import Annotated

from pydantic import Field

from schemas.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=10)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua X, 001', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', example='Rei', max_length=30)]