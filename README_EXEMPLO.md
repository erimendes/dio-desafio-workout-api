⚙️ Exemplos de Conteúdo dos Arquivos
src/app/main.py
from src.app.factory import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)

src/app/factory.py
from fastapi import FastAPI
from src.api.routers import atletas, categorias, centros_treinamento

def create_app() -> FastAPI:
    app = FastAPI(title="Workout API", version="1.0.0")

    # Rotas
    app.include_router(atletas.router, prefix="/atletas", tags=["Atletas"])
    app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
    app.include_router(centros_treinamento.router, prefix="/centros-treinamento", tags=["Centros de Treinamento"])

    return app

src/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.configs.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

src/configs/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Workout API"
    DATABASE_URL: str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()

src/models/base.py
from src.core.database import Base
from sqlalchemy import Column, Integer, DateTime, func

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

src/models/atleta.py
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

src/schemas/atleta.py
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

src/repositories/atleta_repository.py
from sqlalchemy.orm import Session
from src.models.atleta import Atleta
from src.schemas.atleta import AtletaCreate

def listar(db: Session):
    return db.query(Atleta).all()

def criar(db: Session, atleta: AtletaCreate):
    novo = Atleta(**atleta.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

src/api/routers/atletas.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.atleta import AtletaCreate, AtletaResponse
from src.api.controllers.atleta_controller import listar_atletas, criar_atleta

router = APIRouter()

@router.get("/", response_model=list[AtletaResponse])
def listar(db: Session = Depends(get_db)):
    return listar_atletas(db)

@router.post("/", response_model=AtletaResponse)
def criar(atleta: AtletaCreate, db: Session = Depends(get_db)):
    return criar_atleta(db, atleta)

src/api/controllers/atleta_controller.py
from sqlalchemy.orm import Session
from src.repositories import atleta_repository
from src.schemas.atleta import AtletaCreate

def listar_atletas(db: Session):
    return atleta_repository.listar(db)

def criar_atleta(db: Session, atleta: AtletaCreate):
    return atleta_repository.criar(db, atleta)

.env
DATABASE_URL=sqlite:///./workout.db

pyproject.toml
[tool.poetry]
name = "dio-desafio-workout-api"
version = "0.1.0"
description = "API de gerenciamento de atletas, categorias e centros de treinamento."
authors = ["Seu Nome <email@exemplo.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.111.0"
uvicorn = "^0.30.0"
sqlalchemy = "^2.0.30"
pydantic = "^2.8.0"
pydantic-settings = "^2.2.1"

[tool.poetry.dev-dependencies]
pytest = "^8.2.0"
ruff = "^0.5.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

🚀 Como rodar
poetry install
poetry run uvicorn src.app.main:app --reload


Acesse:
👉 http://localhost:8000/docs

Posso gerar pra você um .zip com essa estrutura completa, já com os arquivos e docstrings criados (pronto pra abrir no VSCode ou PyCharm).
Quer que eu gere e te envie o código pronto pra download?