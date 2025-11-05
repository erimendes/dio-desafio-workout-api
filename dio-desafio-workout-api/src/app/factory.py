from fastapi import FastAPI
from src.api.routers import atletas, categorias, centros_treinamento

def create_app() -> FastAPI:
    app = FastAPI(title="Workout API", version="1.0.0")
    app.include_router(atletas.router, prefix="/atletas", tags=["Atletas"])
    app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
    app.include_router(centros_treinamento.router, prefix="/centros-treinamento", tags=["Centros de Treinamento"])
    return app
