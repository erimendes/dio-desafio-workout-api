from pydantic import BaseModel

class AtletaBase(BaseModel):
    nome: str
    idade: int
    categoria_id: int
    centro_treinamento_id: int

class AtletaCreate(AtletaBase):
    pass

class AtletaResponse(AtletaBase):
    id: int
    class Config:
        orm_mode = True
