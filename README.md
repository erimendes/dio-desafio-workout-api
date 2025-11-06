## 🚀 DIO Desafio Workout API

Este projeto é uma **API RESTful** desenvolvida em **Python** utilizando o framework **FastAPI**. Seu objetivo é gerenciar um sistema de cadastro de **atletas e treinos**. A persistência de dados é realizada no **PostgreSQL**, e o gerenciamento do esquema do banco de dados (migrações) é feito com **Alembic**.

### 🌟 Funcionalidades Principais

* Cadastro e Gerenciamento de Atletas
* Gerenciamento de Categorias e Centros de Treinamento
* Controle de Treinos

---

### 🛠️ Configuração e Instalação

#### ⚙️ Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

* **Python (3.12+)**
* **Poetry** (Gerenciador de dependências e ambientes virtuais)
* **Docker** e **Docker Compose** (Recomendado para o PostgreSQL)
* **Git**

#### 📥 Clonar o Projeto

```bash
git clone dio-desafio-workout-api
cd dio-desafio-workout-api
```

🐍 Instalar Python 3 no Ubuntu / Debian (https://wiki.python.org/moin/BeginnersGuide/Download):

🧩 1. Atualize o sistema
```
sudo apt update && sudo apt upgrade -y
```

🏗️ 2. Instale o Python e o pip
```
sudo apt install python3 python3-pip python3-dev -y
```

📦 3 Instalar o pipx
pipx serve para instalar ferramentas Python isoladas (como o Poetry, Flask CLI, etc.)
```
sudo apt install pipx -y
```

🎶 4 Instalar o Poetry com pipx
```
pipx install poetry
poetry --version
```




🚀 Inicialização do Projeto

Inicialize o ambiente e instale todas as dependências necessárias para o projeto.

⚙️ 1. Inicializar o projeto

Se ainda não existir um arquivo pyproject.toml, inicialize o projeto com:

poetry init

📦 2. Instalar dependências de produção

💡 Nota: O pydantic é instalado automaticamente como dependência do FastAPI.

Instale as dependências principais do projeto:

poetry add fastapi uvicorn "sqlalchemy[asyncio]" asyncpg alembic pydantic-settings

🗄️ Configuração do Banco de Dados (PostgreSQL)

É necessário ter um servidor PostgreSQL rodando e acessível na porta 5432.
Recomenda-se o uso de Docker para isolamento e facilidade de configuração.

Subir o container do banco de dados

Certifique-se de que seu docker-compose.yml contém um serviço chamado db.
Para iniciar o container, execute:

docker compose up -d db

🧩 Migrações e Banco de Dados (Alembic)

O Alembic é utilizado para gerenciar a estrutura do banco de dados — criação, atualização e versionamento das tabelas.

🏗️ Inicialização do Alembic

Se ainda não existir a pasta alembic/, inicialize com:

poetry run alembic init alembic

🪄 Geração da Migração Inicial

O comando para gerar as migrações está encapsulado no Makefile.
Ele compara seus modelos Python com o banco de dados e cria o script de migração correspondente.

Gerar a migração inicial com a mensagem "init_db"
make create-migrations d="init_db"

🚚 Aplicar as migrações ao banco

Cria as tabelas e aplica todas as migrações pendentes:

make run-migrations





🗃️ Como acessar o banco de dados (3 maneiras)

Você pode acessar o banco de dados do projeto de três formas diferentes:
via shell do container, pgAdmin ou DBeaver.

🐚 1. Pelo shell do container
Entrar no shell do container
```
docker exec -it workout_db psql -U workout -d workout
```
ou
```
docker exec -it workout_db bash
psql -U workout -d workout
```

Listar as tabelas disponíveis
\dt

🧭 2. Pelo pgAdmin

Se estiver utilizando a interface do pgAdmin, você pode usar a Query Tool para executar comandos SQL.

Listar todas as tabelas no esquema público
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE';

Ver os dados de uma tabela específica (exemplo)
SELECT * FROM atletas;

🖥️ 3. Pelo DBeaver

O DBeaver é uma ferramenta gráfica multiplataforma para gerenciamento de bancos de dados.
Basta configurar uma nova conexão PostgreSQL com as mesmas credenciais do container:

Host: localhost

Porta: 5432

Usuário: workout

Banco: workout


# Estrutura

```
dio-desafio-workout-api/
│
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py    # ponto de entrada FastAPI
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── atletas.py
│   │   │   ├── categorias.py
│   │   │   └── centros_treinamento.py
│   │   └── controllers/    # lógica de negócio separada
│   │       ├── __init__.py
│   │       ├── atleta_controller.py
│   │       ├── categoria_controller.py
│   │       └── centro_treinamento_controller.py
│   │
│   ├── configs/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── database.py (opcional)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── atleta.py
│   │   ├── categoria.py
│   │   ├── centro_treinamento.py
│   │   └── base.py
│   │
│   └── schemas/
│       ├── __init__.py
│       ├── atleta.py
│       ├── categoria.py
│       ├── centro_treinamento.py
│       └── schemas.py
│
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yaml
├── Makefile
├── pyproject.toml
├── poetry.lock
└── README.md
```