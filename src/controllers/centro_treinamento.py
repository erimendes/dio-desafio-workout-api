from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException # Adicionado HTTPException
from pydantic import UUID4
from src.models.centro_treinamento import CentroTreinamentoModel
from src.schemas.centros_treinamento import CentroTreinamentoIn, CentroTreinamentoOut
from src.dependencies import DatabaseDependency
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError # Importado IntegrityError

router = APIRouter()

@router.post(
    '/',
    summary='Criar novo Centro de Treinamento', # Corrigido para plural
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
)
async def post_centro_treinamento(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    """
    Cria um novo centro de treinamento no banco de dados.
    """
    try:
        # Simplificação: Usar model_dump para passar todos os campos do Pydantic para o modelo SQLAlchemy.
        # Remove a geração manual de UUID, confiando no Pydantic ou no modelo.
        centro_treinamento_model = CentroTreinamentoModel(
            **centro_treinamento_in.model_dump() 
        )

        db_session.add(centro_treinamento_model)
        await db_session.commit()
        await db_session.refresh(centro_treinamento_model)

        # Usando model_validate (Pydantic V2)
        return CentroTreinamentoOut.model_validate(centro_treinamento_model, from_attributes=True)

    except IntegrityError:
        # TRATAMENTO DE ERRO: Garante que o usuário receba 409 Conflict em vez de 500 Internal Error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um centro de treinamento com o nome: {centro_treinamento_in.nome}"
        )


@router.get(
    '/',
    summary='Consultar todos os Centros de Treinamento', # Corrigido summary
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query_all(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]: # Função renomeada
    centros_treinamento = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    # Converte a lista de modelos SQLAlchemy para lista de schemas Pydantic
    return [CentroTreinamentoOut.model_validate(ct, from_attributes=True) for ct in centros_treinamento]


@router.get(
    '/{id}',
    summary='Consultar um Centro de Treinamento pelo id', # Corrigido summary
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query_by_id(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut: # Função renomeada
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')

    # Converte o modelo SQLAlchemy para schema Pydantic
    return CentroTreinamentoOut.model_validate(centro_treinamento, from_attributes=True)
