import os
from pathlib import Path
import zipfile
from textwrap import dedent

# ======== CONFIGURAÇÕES ========
ROOT = Path("dio-desafio-workout-api")
SRC = ROOT / "src"

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(dedent(content).strip() + "\n")

# ======== ARQUIVOS PRINCIPAIS ========

def gerar_arquivos_base():
    write_file(ROOT / ".env", """
    DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/workout_db
    ENVIRONMENT=development
    """)

    write_file(ROOT / "Dockerfile", """
    FROM python:3.11-slim
    WORKDIR /app
    RUN apt-get update && apt-get install -y build-essential libpq-dev
    COPY pyproject.toml poetry.lock* /app/
    RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root
    COPY src /app/src
    EXPOSE 8000
    CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    """)

    write_file(ROOT / "docker-compose.yml", """
    version: "3.9"
    services:
      db:
        image: postgres:15
        container_name: workout_db
        restart: always
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: workout_db
        ports:
          - "5432:5432"
        volumes:
          - workout_db_data:/var/lib/postgresql/data

      api:
        build: .
        container_name: workout_api
        restart: always
        depends_on:
          - db
        env_file:
          - .env
        ports:
          - "8000:8000"
        volumes:
          - ./src:/app/src
        command: >
          bash -c "uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload"

    volumes:
      workout_db_data:
    """)

    write_file(ROOT / "Makefile", """
    up:
        docker-compose up --build

    down:
        docker-compose down

    logs:
        docker-compose logs -f api

    bash:
        docker exec -it workout_api /bin/bash

    psql:
        docker exec -it workout_db psql -U postgres -d workout_db
    """)

    write_file(ROOT / "pyproject.toml", """
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
    psycopg2-binary = "^2.9.9"
    pydantic = "^2.8.0"
    pydantic-settings = "^2.2.1"

    [tool.poetry.dev-dependencies]
    pytest = "^8.2.0"
    ruff = "^0.5.0"

    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    """)

    write_file(ROOT / "README.md", """
    # 🏋️‍♂️ DIO Desafio - Workout API

    API construída com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

    ## 🚀 Rodando com Docker

    ```bash
    make up
    ```

    Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)
    """)

# ======== ESTRUTURA SRC ========

def gerar_src():
    # main e factory
    write_file(SRC / "app" / "main.py", """
    from src.app.factory import create_app

    app = create_app()

    if __name__ == "__main__":
        import uvicorn
        uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)
    """)

    write_file(SRC / "app" / "factory.py", """
    from fastapi import FastAPI
    from src.api.routers import atletas, categorias, centros_treinamento

    def create_app() -> FastAPI:
        app = FastAPI(title="Workout API", version="1.0.0")
        app.include_router(atletas.router, prefix="/atletas", tags=["Atletas"])
        app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
        app.include_router(centros_treinamento.router, prefix="/centros-treinamento", tags=["Centros de Treinamento"])
        return app
    """)

    # settings e database
    write_file(SRC / "configs" / "settings.py", """
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        APP_NAME: str = "Workout API"
        DATABASE_URL: str
        ENVIRONMENT: str = "development"

        class Config:
            env_file = ".env"

    settings = Settings()
    """)

    write_file(SRC / "core" / "database.py", """
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
    """)

    # models
    write_file(SRC / "models" / "base.py", """
    from src.core.database import Base
    from sqlalchemy import Column, Integer, DateTime, func

    class BaseModel(Base):
        __abstract__ = True
        id = Column(Integer, primary_key=True, index=True)
        created_at = Column(DateTime(timezone=True), server_default=func.now())
    """)

    write_file(SRC / "models" / "atleta.py", """
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
    """)

    # schemas, repositories, controllers e routers
    write_file(SRC / "schemas" / "atleta.py", """
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
    """)

    write_file(SRC / "repositories" / "atleta_repository.py", """
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
    """)

    write_file(SRC / "api" / "controllers" / "atleta_controller.py", """
    from sqlalchemy.orm import Session
    from src.repositories import atleta_repository
    from src.schemas.atleta import AtletaCreate

    def listar_atletas(db: Session):
        return atleta_repository.listar(db)

    def criar_atleta(db: Session, atleta: AtletaCreate):
        return atleta_repository.criar(db, atleta)
    """)

    write_file(SRC / "api" / "routers" / "atletas.py", """
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
    """)

# ======== ZIPADOR ========
def zip_project():
    zip_path = ROOT.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in ROOT.rglob("*"):
            zipf.write(file, file.relative_to(ROOT.parent))
    print(f"\n✅ Projeto gerado e compactado em: {zip_path.resolve()}")

# ======== EXECUÇÃO ========
if __name__ == "__main__":
    gerar_arquivos_base()
    gerar_src()
    zip_project()
