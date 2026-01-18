"""
César Rodrigues Ribeiro - Desafio Mercado Livre por Arthur 

Rotas da API para busca de produtos e autenticação.

Define todos os endpoints da aplicação, incluindo:
- Busca de produtos
- Autenticação OAuth
- Interface visual
- Health check

"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from typing import Optional
from app.services.produtos_mercadolivre import ProdutosMercadoLivre
from app.services.autenticacao_mercadolivre import AutenticacaoMercadoLivre
from app.schemas.produto import RespostaBusca, Produto
from app.utils.erros import tratar_erro_api, ErroValidacao, ErroAutenticacao
from app.utils.health import verificar_saude

router = APIRouter()
produtos_service = ProdutosMercadoLivre()
auth_service = AutenticacaoMercadoLivre()


@router.get("/", response_class=HTMLResponse)
async def pagina_inicial():

    """  
    Retorna o arquivo index.html:
    """

    index_path = Path(__file__).parent.parent.parent / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    else:
        return HTMLResponse(content="<h1>Arquivo index.html não encontrado</h1>", status_code=404)


@router.get("/api/buscar", response_model=RespostaBusca)
async def buscar_produtos(
    q: str = Query(..., description="Termo de busca", min_length=1),
    limit: int = Query(10, ge=1, le=50)
):

    """
    Busca produtos no Mercado Livre (todos os status).
    Use os filtros da interface para filtrar por status específico.
    Sempre retorna o mesmo formato de resposta.

    """

    resultado = produtos_service.buscar_produtos(q, limit)


    # Mesmo em erro, o schema é respeitado
    return {
        "total": resultado.get("total", 0),
        "produtos": resultado.get("produtos", []),
        "erro": resultado.get("erro")
    }



@router.get("/api/autorizar")
async def obter_url_autorizacao():

    """    

    Returns:
        URL de autorização OAuth

    """

    try:
        url = auth_service.gerar_url_autorizacao()
        return {
            "url_autorizacao": url,
            "mensagem": "Acesse a URL acima para autorizar a aplicação"
        }
    except ValueError as e:
        raise ErroValidacao(str(e))
    except Exception as e:
        raise tratar_erro_api(e)


@router.get("/api/callback")
async def callback_oauth(code: Optional[str] = None):
    """
    
    Endpoint de callback para receber o código de autorização OAuth.
    
    Args:
        code: Código de autorização retornado pelo Mercado Livre
    
    Returns:
        Tokens de autenticação


    """
    if not code:
        raise ErroValidacao("Código de autorização não fornecido")
    
    try:
        token_data = auth_service.trocar_codigo_por_token(code)
        return {
            "mensagem": "Autenticação realizada com sucesso!",
            "access_token": token_data.get("access_token"),
            "refresh_token": token_data.get("refresh_token"),
            "expires_in": token_data.get("expires_in"),
            "instrucoes": "Adicione ML_ACCESS_TOKEN e ML_REFRESH_TOKEN ao arquivo .env"
        }
    except Exception as e:
        raise tratar_erro_api(e)


@router.get("/api/saude")
async def health_check():
    """

    Endpoint de health check da aplicação.
    
    Returns:
        Status de saúde da aplicação


    """
    return verificar_saude()
