# /src/main.py
from fastapi import FastAPI
from src.routers import atletas
from src.routers import categorias
from src.routers import centro_treinamento

# IMPORTAÇÃO CRÍTICA PARA O SQLALCHEMY (Solução do problema)
# Isso garante que todas as classes que herdam de BaseModel (como AtletaModel e CategoriaModel)
# sejam carregadas e registradas no Metadata do SQLAlchemy antes que os relacionamentos sejam configurados.
# Ajuste os nomes dos módulos conforme sua estrutura de pastas (ex: src.models.atleta)
import src.models.atleta
import src.models.categorias
# O modelo CentroTreinamentoModel precisa ser importado também para que o relacionamento em AtletaModel funcione.
import src.models.centro_treinamento 


# Inicializa a aplicação principal FastAPI
app = FastAPI(
    title="WorkoutApi",
    version="0.1.0",
    description="API para um sistema de gestão de treinos."
)

# Inclui o roteador principal que agrega todos os endpoints
app.include_router(categorias.api_router)
app.include_router(atletas.api_router)
app.include_router(centro_treinamento.api_router)

# Para rodar a aplicação (Descomente este bloco ou execute via linha de comando)
# if __name__ == '__main__':
#     import uvicorn
#     # Use 'main:app' para referenciar o objeto 'app' no arquivo 'main.py'
#     uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True)
