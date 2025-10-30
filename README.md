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

# Comando: Aplica todas as migrações pendentes no banco
make run-migrations

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