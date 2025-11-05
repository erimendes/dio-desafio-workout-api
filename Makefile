# Variável principal para definir o comando Poetry
POETRY_RUN = poetry run

# ----------------------------------------------------
# 1. Execução da Aplicação
# ----------------------------------------------------
run:
	$(POETRY_RUN) uvicorn src.app.main:app --reload

# ----------------------------------------------------
# 2. Migrações do Alembic
# ----------------------------------------------------
# Comando para criar uma nova migração (use: make create-migrations d="nome da migracao")
create-migrations:
	# O Poetry Run garante que o Alembic seja executado no ambiente virtual
	$(POETRY_RUN) alembic revision --autogenerate -m "$(d)"

# Comando para aplicar todas as migrações pendentes ao banco de dados
run-migrations:
	$(POETRY_RUN) alembic upgrade head
