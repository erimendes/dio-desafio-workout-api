# src/controllers/categoria.py
from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4
from src.models.categorias import CategoriaModel
from src.schemas.categorias import CategoriaIn, CategoriaOut
from src.api.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/',
    summary='Criar nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut
)
async def post_categoria(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    # Criar ID único
    categoria_id = uuid4()

    # Criar instância do SQLAlchemy
    categoria_model = CategoriaModel(
        id=categoria_id,
        nome=categoria_in.nome  # ou outros campos de CategoriaIn
    )

    # Adicionar ao banco
    db_session.add(categoria_model)
    await db_session.commit()
    await db_session.refresh(categoria_model)  # importante para pegar dados atualizados do DB

    # Retornar como Pydantic
    return CategoriaOut.from_orm(categoria_model)

@router.get(
    '/',
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias

@router.get(
    '/{id}',
    summary='Consultar uma categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no id: {id}')

    return categoria