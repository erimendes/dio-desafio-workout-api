# src/controllers/atleta.py

from datetime import datetime, timezone
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4, ValidationError
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Type # Importação útil para tipagem de classes de modelo

# Importações dos modelos e schemas
from src.models.atleta import AtletaModel
from src.models.categorias import CategoriaModel
from src.models.centro_treinamento import CentroTreinamentoModel
from src.schemas.atleta import AtletaIn, AtletaOut, AtletaUpdate
from src.api.dependencies import DatabaseDependency

router = APIRouter()

# --- FUNÇÃO AUXILIAR DE REUSO (BOA PRÁTICA) ---
async def get_entity_or_400(
    db_session: DatabaseDependency, 
    model: Type[CategoriaModel | CentroTreinamentoModel], 
    nome: str, 
    entity_name: str
):
    """
    Busca uma entidade (Categoria ou CT) pelo nome e levanta um 
    HTTPException 400 se não for encontrada.
    """
    entity = (await db_session.execute(
        select(model).filter_by(nome=nome)
    )).scalars().first()
    
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{entity_name} '{nome}' não encontrado(a)."
        )
    return entity

# --- ROTA: POST / ---
@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post_atleta(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    """
    Cria um novo atleta, validando a existência da Categoria e do Centro de Treinamento.
    """

    # 1. Busca e validação de entidades relacionadas (Refatorado com função auxiliar)
    categoria = await get_entity_or_400(
        db_session, CategoriaModel, atleta_in.categoria.nome, "Categoria"
    )
    centro_treinamento = await get_entity_or_400(
        db_session, CentroTreinamentoModel, atleta_in.centro_treinamento.nome, "Centro de Treinamento"
    )

    # 2. Criação do modelo Atleta
    # A validação de input é feita pelo FastAPI/Pydantic.
    atleta_data = atleta_in.model_dump(exclude={"categoria", "centro_treinamento"})
    atleta_model = AtletaModel(
        **atleta_data,
        categoria_id=categoria.pk_id,
        centro_treinamento_id=centro_treinamento.pk_id,
        # Opcional, mas útil para relações ORM:
        categoria=categoria,
        centro_treinamento=centro_treinamento,
    )

    # 3. Persistência no banco de dados e tratamento de erros
    try:
        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)
    
    except IntegrityError:
        # Uso de 409 CONFLICT, mais semântico que 303 SEE_OTHER para chaves duplicadas.
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}"
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados: {str(e)}"
        )

    return AtletaOut.model_validate(atleta_model)

# --- ROTA: GET / (Todos) ---
@router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut]
)
async def query_all(db_session: DatabaseDependency) -> list[AtletaOut]:
    """Consulta e retorna a lista de todos os atletas."""
    atletas: list[AtletaModel] = (await db_session.execute(select(AtletaModel))).scalars().all()
    # Converte os modelos ORM (AtletaModel) para o schema de saída (AtletaOut)
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

# --- ROTA: GET /{id} (Individual) ---
@router.get(
    '/{id}',
    summary='Consultar um atleta pelo id', 
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query_one(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    """Consulta e retorna um atleta específico pelo seu ID (UUID)."""
    
    atleta: AtletaModel = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        # Usando Atleta/404 NOT FOUND com detalhe correto
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )

    # Retorna o modelo ORM, permitindo que o Pydantic o valide contra AtletaOut
    return atleta

# --- ROTA: PATCH /{id} ---
@router.patch(
    '/{id}',
    summary='Alterar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)):
    """Atualiza os dados de um atleta pelo ID, permitindo apenas campos fornecidos."""
    
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )

    # Uso de 'exclude_unset=True' para garantir que apenas os 
    # campos passados na requisição sejam atualizados, ignorando os não definidos.
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    
    # Aplica as atualizações no modelo ORM
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    # Deve-se passar o objeto 'atleta' para o refresh
    await db_session.refresh(atleta) 
    
    return atleta # Retorna o objeto atualizado

# --- ROTA: DELETE /{id} ---
@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo id',
    # Padrão escolhido: Status 200 OK, retornando o objeto que foi deletado.
    status_code=status.HTTP_200_OK, 
    response_model=AtletaOut
)
# Tipagem de retorno é AtletaOut (o que será retornado)
async def delete_atleta(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    """Deleta um atleta pelo ID e retorna o objeto excluído."""
    
    atleta: AtletaModel = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    # Cria o modelo de resposta (AtletaOut) ANTES de deletar, pois depois da deleção 
    # o objeto ORM pode estar em um estado inválido para validação.
    atleta_out = AtletaOut.model_validate(atleta) 

    await db_session.delete(atleta)
    await db_session.commit()
    
    return atleta_out # Retorna o objeto deletado