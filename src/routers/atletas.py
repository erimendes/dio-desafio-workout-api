# dio-desafio-workout-api/src/routers/atletas.py
from fastapi import APIRouter
from src.controllers.atleta import router as atleta_router

# CORREÇÃO CHAVE: Você deve instanciar APIRouter chamando-o com parênteses!
api_router = APIRouter()

# Inclui o roteador de atletas sob o prefixo /atletas
api_router.include_router(atleta_router, prefix='/atletas', tags=['atletas'])

