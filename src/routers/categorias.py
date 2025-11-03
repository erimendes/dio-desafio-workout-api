# dio-desafio-workout-api/src/routers/categorias.py
from fastapi import APIRouter
from src.controllers.categoria import router as categoria_router

# CORREÇÃO CHAVE: Você deve instanciar APIRouter chamando-o com parênteses!
api_router = APIRouter()

api_router.include_router(categoria_router, prefix='/categorias', tags=['categorias'])