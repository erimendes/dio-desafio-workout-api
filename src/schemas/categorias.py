from typing import Annotated

from pydantic import Field
from schemas.schemas import BaseSchema

class Categorias(BaseSchema):
    nome: Annotated[str, Field(description='Nome da Categoria', example='Scale', max_length=10)]