from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException # Adicionado HTTPException
from pydantic import UUID4
from src.models.centro_treinamento import CentroTreinamentoModel
from src.schemas.centros_treinamento import CentroTreinamentoIn, CentroTreinamentoOut, CentroTreinamentoPatch
from src.api.dependencies import DatabaseDependency
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError # Importado IntegrityError


router = APIRouter()

@router.post(
    '/',
    summary='Criar novo Centro de Treinamento',
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
        centro_treinamento_out = CentroTreinamentoOut(
            id=uuid4(), 
            **centro_treinamento_in.model_dump()
        )
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
    summary='Consultar todos os Centros de Treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query_all(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento_out: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    # Converte a lista de modelos SQLAlchemy para lista de schemas Pydantic
    return [CentroTreinamentoOut.model_validate(ct, from_attributes=True) for ct in centros_treinamento_out]


@router.get(
    '/{id}',
    summary='Consultar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query_by_id(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')

    # Converte o modelo SQLAlchemy para schema Pydantic
    return CentroTreinamentoOut.model_validate(centro_treinamento, from_attributes=True)


# --- ENDPOINT PATCH ---
@router.patch(
    '/{id}',
    summary='Atualizar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def patch_centro_treinamento(
    id: UUID4, 
    db_session: DatabaseDependency, 
    # Usar o schema de Patch
    centro_treinamento_in: CentroTreinamentoPatch = Body(...) 
) -> CentroTreinamentoOut:
    # 1. Buscar o centro de treinamento
    centro_treinamento: CentroTreinamentoModel = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')

    try:
        # 2. Aplicar a atualização parcial
        # model_dump(exclude_unset=True) pega APENAS os campos que foram fornecidos no body.
        update_data = centro_treinamento_in.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(centro_treinamento, key, value)

        # 3. Salvar e atualizar
        await db_session.commit()
        await db_session.refresh(centro_treinamento)

        return CentroTreinamentoOut.model_validate(centro_treinamento, from_attributes=True)

    except IntegrityError:
        # Certifique-se de que o campo 'nome' está na requisição para não dar erro aqui
        nome_tentado = centro_treinamento_in.nome if centro_treinamento_in.nome else "Um nome" 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um centro de treinamento com o nome: {nome_tentado}"
        )
    
# --- ENDPOINT DELETE (Exclusão) ---
@router.delete(
    '/{id}',
    summary='Deletar um Centro de Treinamento pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_centro_treinamento(id: UUID4, db_session: DatabaseDependency) -> None:
    # 1. Buscar o centro de treinamento
    centro_treinamento: CentroTreinamentoModel = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    
    if not centro_treinamento:
        # Mesmo no DELETE, se o recurso não for encontrado, é bom retornar 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')

    # 2. Remover do banco
    await db_session.delete(centro_treinamento)
    await db_session.commit()
    
    # Retorna 204 No Content (corpo vazio), conforme o padrão REST para DELETE
    return