"""
Utilitários para verificação de saúde da aplicação.

Fornece endpoints de health check para monitoramento
e diagnóstico da aplicação.
"""
from datetime import datetime
from typing import Dict, Any


def verificar_saude() -> Dict[str, Any]:
    """
    Retorna o status de saúde da aplicação.
    
    Returns:
        Dicionário com informações de status
    """
    return {
        "status": "saudavel",
        "timestamp": datetime.now().isoformat(),
        "mensagem": "API do Desafio Mercado Livre funcionando",
        "versao": "1.0.1"
    }
