# src/controllers/atleta.py
from datetime import datetime, timezone
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4, ValidationError
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.models.atleta import AtletaModel
from src.models.categorias import CategoriaModel
from src.models.centro_treinamento import CentroTreinamentoModel
from src.schemas.atleta import AtletaIn, AtletaOut, AtletaUpdate
from src.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post_atleta(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    """Cria um novo atleta, validando a existência da Categoria e do Centro de Treinamento."""

    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome)
    )).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria '{categoria_nome}' não encontrada."
        )

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
    )).scalars().first()
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Centro de Treinamento '{centro_treinamento_nome}' não encontrado."
        )

    try:
        atleta_data = atleta_in.model_dump(exclude={"categoria", "centro_treinamento"})
        atleta_model = AtletaModel(
            **atleta_data,
            categoria_id=categoria.pk_id,
            centro_treinamento_id=centro_treinamento.pk_id,
            categoria=categoria,
            centro_treinamento=centro_treinamento,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors()
        )

    try:
        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}"
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados: {str(e)}"
        )

    return AtletaOut.model_validate(atleta_model)

@router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut]
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
    '/{id}',
    summary='Consultar um atleta pelo id', # CORRIGIDO: de 'categoria' para 'atleta'
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}' # CORRIGIDO: de 'Categoria' para 'Atleta'
        )

    return atleta

@router.patch(
        '/{id}',
        summary='Alterar uma atleta pelo id',
        status_code=status.HTTP_200_OK, # Status 200 porque retorna um corpo
        response_model=AtletaOut)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)):
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(404, f'Atleta não encontrado no id: {id}')

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)
    return AtletaOut.model_validate(atleta)

# ...
@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_200_OK, # Status 200 porque retorna um corpo
    response_model=AtletaOut
)
async def delete_atleta(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    atleta_out = AtletaOut.model_validate(atleta) # Cria o modelo de resposta antes de deletar

    await db_session.delete(atleta)
    await db_session.commit()
    
    return atleta_out # Retorna o objeto deletado