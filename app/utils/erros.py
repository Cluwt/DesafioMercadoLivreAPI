"""
Utilitários para tratamento de erros customizados.

Fornece exceções personalizadas e funções para converter
erros em respostas HTTP amigáveis ao usuário.
"""
from fastapi import HTTPException
from typing import Optional


class ErroAPI(Exception):
    """
    Exceção customizada para erros da API.
    
    Permite associar um código de status HTTP específico
    a cada tipo de erro.
    """
    def __init__(self, mensagem: str, status_code: int = 500):
        """
        Args:
            mensagem: Mensagem de erro amigável ao usuário
            status_code: Código HTTP de status
        """
        self.mensagem = mensagem
        self.status_code = status_code
        super().__init__(self.mensagem)


class ErroAutenticacao(ErroAPI):
    """Erro relacionado à autenticação."""
    def __init__(self, mensagem: str = "Erro de autenticação"):
        super().__init__(mensagem, status_code=401)


class ErroValidacao(ErroAPI):
    """Erro relacionado à validação de dados."""
    def __init__(self, mensagem: str = "Dados inválidos"):
        super().__init__(mensagem, status_code=400)


class ErroRecursoNaoEncontrado(ErroAPI):
    """Erro quando um recurso não é encontrado."""
    def __init__(self, mensagem: str = "Recurso não encontrado"):
        super().__init__(mensagem, status_code=404)


def tratar_erro_api(erro: Exception) -> HTTPException:
    """
    Converte exceções em respostas HTTP amigáveis.
    
    Garante que erros técnicos não sejam expostos ao usuário,
    seguindo as boas práticas de segurança.
    
    Args:
        erro: Exceção capturada
        
    Returns:
        HTTPException formatada para resposta
    """
    if isinstance(erro, ErroAPI):
        return HTTPException(
            status_code=erro.status_code,
            detail=erro.mensagem
        )
    
    # Erros genéricos não expõem detalhes técnicos
    return HTTPException(
        status_code=500,
        detail="Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde."
    )
