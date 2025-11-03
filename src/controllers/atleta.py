# src/controllers/atleta.py
from datetime import datetime
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import ValidationError
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.models.atleta import AtletaModel
from src.models.categorias import CategoriaModel
from src.models.centro_treinamento import CentroTreinamentoModel
from src.schemas.atleta import AtletaIn, AtletaOut
from src.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut # Alterado para retornar o schema de saída AtletaOut
)
async def post_atleta(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    """
    Cria um novo atleta, validando a existência da Categoria e do Centro de Treinamento.
    """
    # 1. Busca Categoria e CT para garantir que existem
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    
    # Busca a Categoria
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome)
    )).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria '{categoria_nome}' não encontrada."
        )

    # Busca o Centro de Treinamento
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
    )).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Centro de Treinamento '{centro_treinamento_nome}' não encontrado."
        )

    # 2. Converte Pydantic para Modelo SQLAlchemy
    try:
        # Cria um dicionário com os dados do atleta, substituindo os schemas aninhados
        # pelos objetos ou IDs necessários para o Modelo do SQLAlchemy.
        atleta_data = atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'})
        
        atleta_model = AtletaModel(
            **atleta_data,
            created_at=datetime.utcnow(),
            categoria_id=categoria.pk_id,
            centro_treinamento_id=centro_treinamento.pk_id,
            categoria=categoria, # Opcional, mas ajuda a manter o objeto atualizado
            centro_treinamento=centro_treinamento # Opcional
        )
    except ValidationError as e:
        # Se houver erro de validação (embora o Pydantic já faça isso), tratamos
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors()
        )
    
    # 3. Persistência (Adicionar e Commitar)
    try:
        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)
    except IntegrityError:
        # Trata erros como CPF duplicado
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}"
        )
    except Exception:
        # Outros erros de banco de dados
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao inserir os dados no banco."
        )

    # 4. Retorna o Atleta criado
    # É necessário usar AtletaOut.model_validate(atleta_model) ou .from_orm() 
    # para conversão correta se você usa o SQLAlchemy ORM Mode no Pydantic.
    return AtletaOut.model_validate(atleta_model) 
