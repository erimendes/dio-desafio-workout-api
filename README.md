🚀 DIO Desafio Workout API

Este projeto é uma API desenvolvida em Python, utilizando o framework FastAPI, para gerenciar um sistema de cadastro de atletas e treinos, com persistência de dados no PostgreSQL e gerenciamento de esquema via Alembic.

🛠️ Configuração e Instalação

Pré-requisitos

Certifique-se de ter o Python (3.12+) e o Poetry instalados.

1. Inicialização do Projeto

Inicialize o ambiente e instale todas as dependências do projeto:

# Inicializa o projeto (se ainda não tiver um pyproject.toml)
poetry init 

# Instala todas as dependências de produção
# Nota: O pydantic é instalado automaticamente como dependência do FastAPI.
poetry add fastapi uvicorn 'sqlalchemy[asyncio]' asyncpg alembic


2. Configuração do Banco de Dados (PostgreSQL)

É necessário ter um servidor PostgreSQL rodando e acessível na porta 5432. Recomenda-se o uso de Docker para isolamento do ambiente.

Crie um container Docker para o PostgreSQL (Seu docker-compose.yml deve conter o serviço db):

# Exemplo de comando Docker para iniciar apenas o serviço de banco de dados
docker compose up -d db 


⚙️ Migrações e Banco de Dados (Alembic)

O Alembic é utilizado para gerenciar o esquema do banco de dados (criação e alteração de tabelas).

1. Inicialização do Alembic

Se você ainda não tiver a pasta alembic/, execute:

poetry run alembic init alembic


2. Geração da Migração Inicial

O comando para gerar migrações está encapsulado no Makefile. Este processo compara seus modelos Python com o banco de dados e cria o script de migração.

# Comando: Gera a migração com a mensagem "init_db"
# (Assume que seu Makefile está corrigido e usando poetry run)
make create-migrations d="init_db" 


3. Aplicação da Migração

Após gerar o arquivo de migração, aplique-o no banco de dados.

# Comando: Aplica todas as migrações pendentes no banco(Cria as tabelas)
Gerenciamento e Verificação do Banco de Dados PostgreSQL

Este guia contém os comandos essenciais para aplicar migrações e verificar o estado das tabelas diretamente no container.

1. Aplicar Migrações (Criar as Tabelas)

Use o comando do Makefile para aplicar todas as migrações pendentes no banco de dados (workout), criando as tabelas definidas nos seus modelos.

# Comando: Aplica todas as migrações pendentes no banco (Cria as tabelas)
make run-migrations


2. Confirmar as Tabelas no Container

Após aplicar a migração, você pode entrar no container do PostgreSQL para confirmar se as tabelas (atletas, categorias, etc.) foram criadas.

Opção A: Acesso Direto (Recomendado)

Use o comando docker exec para se conectar diretamente ao cliente psql dentro do container.

# O nome do container é 'workout_db' (definido no docker-compose.yml)
# -U: Usuário | -d: Banco de Dados
docker exec -it workout_db psql -U workout -d workout


Atenção: Você será solicitado a fornecer a senha (POSTGRES_PASSWORD do seu arquivo .env).

Após logar, use o meta-comando para listar as tabelas:

\dt


Opção B: Acesso em Duas Etapas

Entra primeiro no shell do container e depois no cliente psql.

# 1. Entrar no shell do container
docker exec -it workout_db bash

# 2. Conectar ao psql a partir do shell
psql -U workout -d workout

# 3. Listar as tabelas
\dt 


3. Consultar as Tabelas pelo pgAdmin

Se estiver usando a interface do pgAdmin, você pode usar a Query Tool:

-- Query SQL para listar todas as tabelas no esquema público
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE';


Ou, para ver os dados de uma tabela específica (exemplo):

SELECT * FROM atletas;

```
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

# Instalar pydantic-settings
poetry add pydantic-settings

# Instalar o DBeaver para gerenciar o banco de dados


# Estrutura
```
.
├── dio-desafio-workout-api/
│   ├──src/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/  # Rotas e funções de API (APIRouter)
│   │   │   │   │   ├── user.py
│   │   │   │   │   ├── item.py
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py             # Configurações globais (Settings com Pydantic)
│   │   │   ├── dependencies.py       # Dependências reutilizáveis (Auth, Sessão DB)
│   │   │   └── __init__.py
│   │   │
│   │   ├── db/
│   │   │   ├── base.py               # Configurações de conexão DB (Engine/Session)
│   │   │   ├── crud.py               # Operações de CRUD de baixo nível
│   │   │   └── __init__.py
│   │   │
│   │   ├── controllers/
│   │   │
│   │   ├── models/
│   │   │   ├── user.py               # Modelos ORM (SQLModel/SQLAlchemy)
│   │   │   ├── item.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py               # Modelos de validação de dados (Pydantic)
│   │   │   ├── item.py               # (Entrada/Saída de dados da API)
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/
│   │   │   ├── user.py               # Lógica de Negócios (Business Logic)
│   │   │   ├── item.py               # (Isola a rota da complexidade)
│   │   │   └── __init__.py
│   │   │
│   │   ├── views/
│   │   │
│   │   └── main.py                   # Ponto de entrada da aplicação FastAPI
│   │
├── tests/                        # Arquivos de Teste
│   ├── conftest.py
│   ├── test_user.py
│   └── test_item.py
│
├── .env                          # Variáveis de ambiente
├── requirements.txt              # Dependências do Python
└── Dockerfile                    # Containerização
```