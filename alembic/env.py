# Importa o módulo asyncio para lidar com operações assíncronas (necessário para usar async/await)
import asyncio

# Importa utilitário para configurar logging a partir de um arquivo de configuração (ex: alembic.ini)
from logging.config import fileConfig

# Importa tipos e classes do SQLAlchemy necessários para migrações assíncronas
from sqlalchemy.engine import Connection               # Tipo de conexão (pode ser usado com run_sync)
from sqlalchemy.ext.asyncio import async_engine_from_config  # Cria um "engine" assíncrono a partir do arquivo de config
from sqlalchemy import pool                            # Gerenciamento de conexões (pooling)

# Importa o objeto de contexto do Alembic, responsável por coordenar as migrações
from alembic import context

import sys
import os

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# 1. Importa a Base (do models.py)
from models.base import BaseModel 

# 2. Importa TODOS os arquivos de modelo para popular o target_metadata
#    (Mesmo que eles não sejam usados diretamente aqui, eles precisam ser carregados)
from src.models.atleta import AtletaModel
from src.models.categorias import CategoriaModel
from src.models.centro_treinamento import CentroTreinamentoModel # Adicione outros modelos se houver

# Carrega o objeto de configuração principal do Alembic, obtendo as definições do alembic.ini
config = context.config

# Se existir um arquivo de configuração de logging (geralmente alembic.ini),
# inicializa o sistema de logs do Alembic.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define qual metadado (metadata) o Alembic deve usar para autogerar migrações.
# Esse metadata contém todas as definições de tabelas e colunas do seu modelo ORM.
target_metadata = BaseModel.metadata


# ===============================================================
# MODO OFFLINE (gera SQLs sem conectar no banco)
# ===============================================================
def run_migrations_offline() -> None:
    """Executa migrações em modo 'offline' — ou seja, gera o SQL sem se conectar ao banco."""

    # Obtém a URL do banco de dados a partir do alembic.ini
    url = config.get_main_option("sqlalchemy.url")

    # Configura o contexto do Alembic para o modo offline, com parâmetros estáticos
    context.configure(
        url=url,                              # Define a URL de conexão
        target_metadata=target_metadata,      # Define o metadata do ORM
        literal_binds=True,                   # Insere valores diretamente no SQL
        dialect_opts={"paramstyle": "named"}, # Define o estilo de parâmetros
    )

    # Inicia uma transação e executa as migrações (gera o SQL de alteração de schema)
    with context.begin_transaction():
        context.run_migrations()


# ===============================================================
# Função auxiliar para executar migrações dentro de uma conexão
# ===============================================================
def do_run_migrations(connection: Connection) -> None:
    """Executa as migrações usando uma conexão existente (sincronamente dentro do async)."""

    # Configura o contexto do Alembic com a conexão e o metadata do ORM
    context.configure(connection=connection, target_metadata=target_metadata)

    # Inicia a transação e aplica as migrações
    with context.begin_transaction():
        context.run_migrations()


# ===============================================================
# MODO ONLINE ASSÍNCRONO (executa diretamente no banco)
# ===============================================================
async def run_async_migrations():
    """Cria engine assíncrono e executa migrações no banco de dados real."""

    # Cria um "engine" assíncrono (objeto que gerencia as conexões ao banco)
    # usando as configurações definidas no alembic.ini (seção sqlalchemy.*)
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),  # Lê a seção "alembic" do arquivo ini
        prefix="sqlalchemy.",                               # Lê apenas as chaves que começam com "sqlalchemy."
        poolclass=pool.NullPool,                            # Não usa pool de conexões (cria e fecha cada vez)
    )

    # Abre uma conexão assíncrona com o banco de dados
    async with connectable.connect() as connection:
        # Executa as migrações de forma síncrona dentro do contexto assíncrono
        # O Alembic internamente precisa de operações síncronas, então usamos run_sync
        await connection.run_sync(do_run_migrations)


# ===============================================================
# Função principal para decidir qual modo usar
# ===============================================================
def run_migrations_online() -> None:
    """Executa migrações em modo 'online' usando asyncio (modo padrão ao rodar `alembic upgrade head`)."""

    # Executa a função assíncrona principal dentro do loop de eventos do asyncio
    asyncio.run(run_async_migrations())


# ===============================================================
# Escolhe entre modo OFFLINE e ONLINE
# ===============================================================
if context.is_offline_mode():
    # Se o Alembic for chamado com `--sql`, roda em modo offline
    run_migrations_offline()
else:
    # Caso contrário, conecta ao banco e aplica as migrações
    run_migrations_online()



# import asyncio
# from logging.config import fileConfig

# # 30-10-2025 - Alteração
# # from sqlalchemy import Connection, engine_from_config
# from sqlalchemy import Connection
# from sqlalchemy.ext.asyncio import async_engine_from_config
# from sqlalchemy import pool

# from alembic import context
# # 30-10-2025 - Alteração
# from models.models import *

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata

# # 30-10-2025 - Alteração
# target_metadata = BaseModel.metadata

# # other values from the config, defined by the needs of env.py,
# # can be acquired:
# # my_important_option = config.get_main_option("my_important_option")
# # ... etc.


# def run_migrations_offline() -> None:
#     """Run migrations in 'offline' mode.

#     This configures the context with just a URL
#     and not an Engine, though an Engine is acceptable
#     here as well.  By skipping the Engine creation
#     we don't even need a DBAPI to be available.

#     Calls to context.execute() here emit the given string to the
#     script output.

#     """
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )

#     with context.begin_transaction():
#         context.run_migrations()

# # 30-10-2025 - Alteração
# def do_run_migrations(connection: Connection) -> None:
#     context.configure(connection=connection, target_metadata=target_metadata)

#     with context.begin_transaction():
#         context.run_migrations()

# async def run_async_migrations():
#     connectable = async_engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)

# def run_migrations_online() -> None:
#     """Run migrations in 'online' mode.

#     In this scenario we need to create an Engine
#     and associate a connection with the context.

#     """
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata
#         )

#         with context.begin_transaction():
#             context.run_migrations()

# def run_migrations_online():
#     asyncio.run(run_async_migrations)

# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()
