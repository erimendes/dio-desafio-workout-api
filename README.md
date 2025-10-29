# dio-desafio-workout-api
# Instalações basicas
poetry add fastapi uvicorn aqlalchemy
# O pydantic é instalado quando se instala o fastapi

# Estrutura
```
.
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/  # Rotas e funções de API (APIRouter)
│   │   │   │   ├── user.py
│   │   │   │   ├── item.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py             # Configurações globais (Settings com Pydantic)
│   │   ├── dependencies.py       # Dependências reutilizáveis (Auth, Sessão DB)
│   │   └── __init__.py
│   │
│   ├── db/
│   │   ├── base.py               # Configurações de conexão DB (Engine/Session)
│   │   ├── crud.py               # Operações de CRUD de baixo nível
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── user.py               # Modelos ORM (SQLModel/SQLAlchemy)
│   │   ├── item.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── user.py               # Modelos de validação de dados (Pydantic)
│   │   ├── item.py               # (Entrada/Saída de dados da API)
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── user.py               # Lógica de Negócios (Business Logic)
│   │   ├── item.py               # (Isola a rota da complexidade)
│   │   └── __init__.py
│   │
│   └── main.py                   # Ponto de entrada da aplicação FastAPI
│
├── tests/                        # Arquivos de Teste
│   ├── conftest.py
│   ├── test_user.py
│   └── test_item.py
│
├── .env                          # Variáveis de ambiente
├── requirements.txt              # Dependências do Python
└── Dockerfile                    # Containerização
```