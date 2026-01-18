"""
Aplicação principal FastAPI para o Desafio Mercado Livre.

Esta aplicação consome a API do Mercado Livre para buscar produtos ativos
e exibi-los em formato de cards visuais, incluindo autenticação OAuth.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.api.routes import router

# Criar instância da aplicação FastAPI
app = FastAPI(
    title="Desafio Mercado Livre - API de Produtos",
    description="""


 API desenvolvida para o desafio técnico de integração com Mercado Livre.


## Funcionalidades Principais

* **Busca de Produtos**: Busca produtos ativos no Mercado Livre
* **Autenticação OAuth**: Gerencia autenticação OAuth 2.0 completa
* **Interface Visual**: Interface web moderna para visualização de produtos
* **Tratamento de Erros**: Tratamento robusto de erros com mensagens amigáveis

## Endpoints Disponíveis

* **GET /**: Interface visual para busca de produtos
* **GET /api/buscar**: Endpoint de busca de produtos (JSON)
* **GET /api/autorizar**: Obtém URL de autorização OAuth
* **GET /api/callback**: Callback OAuth para receber tokens
* **GET /api/saude**: Health check da aplicação

## Como Usar

1. Acesse a interface visual em **GET /**
2. Use **/api/buscar** para buscar produtos via JSON
3. Configure OAuth com **/api/autorizar** e **/api/callback**


""",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar arquivos estáticos
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Incluir rotas da API
app.include_router(router)

# Endpoint raiz alternativo (redireciona para a interface)
@app.get("/api")
def api_info():
    """
    Informações sobre a API.
    """
    return {
        "mensagem": "Bem-vindo(a) à API do Desafio Mercado Livre!",
        "versao": "1.0.1",
        "endpoints": {
            "interface": "/",
            "buscar_produtos": "/api/buscar?q=<termo>",
            "autorizar": "/api/autorizar",
            "callback": "/api/callback?code=<codigo>",
            "saude": "/api/saude",
            "documentacao": "/docs"
        },
        "instrucoes": "Acesse / para ver a interface visual ou /docs para a documentação completa da API"
    }

@router.get("/api/callback")
def callback(code: str):
    return {"code": code}

