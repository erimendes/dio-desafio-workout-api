# src/configs/database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.configs.settings import settings

# Cria o engine assíncrono
engine = create_async_engine(settings.DB_URL, echo=False)

# Cria uma factory de sessões assíncronas
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependência para FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session