# src/routers/centro_treinamento.py
from fastapi import APIRouter
from src.controllers.centro_treinamento import router as centro_treinamento_router

api_router = APIRouter()

api_router.include_router(
    centro_treinamento_router, 
    prefix='/centro_treinamento', 
    tags=['Centros de treinamento']
)