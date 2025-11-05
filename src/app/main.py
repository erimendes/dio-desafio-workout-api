# /src/main.py
from fastapi import FastAPI
from src.api.routers.routers import api_router

# Inicializa a aplicação principal FastAPI
app = FastAPI(
    title="WorkoutApi",
    version="0.1.0",
    description="API para um sistema de gestão de treinos."
)

# Inclui o roteador principal que agrega todos os endpoints
app.include_router(api_router)
