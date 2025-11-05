from fastapi import APIRouter

from src.api.controllers.atleta import router as atleta_router
from src.api.controllers.categoria import router as categoria_router
from src.api.controllers.centro_treinamento import router as centro_treinamento_router 
api_router = APIRouter()
api_router.include_router(atleta_router, prefix="/atletas", tags=["Atletas"])
api_router.include_router(categoria_router, prefix="/categorias", tags=["Categorias"])
api_router.include_router(centro_treinamento_router, prefix="/centros-treinamento",
                      tags=["Centros de Treinamento"])

