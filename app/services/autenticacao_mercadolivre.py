"""
Serviço de autenticação OAuth com a API do Mercado Livre.

Responsável por:
- Gerar a URL de autorização OAuth
- Trocar o authorization code por um access_token
"""

import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class AutenticacaoMercadoLivre:
    def __init__(self) -> None:
        self.client_id: str | None = os.getenv("ML_CLIENT_ID")
        self.client_secret: str | None = os.getenv("ML_CLIENT_SECRET")
        self.redirect_uri: str | None = os.getenv("ML_REDIRECT_URI")
        self.access_token: str | None = os.getenv("ML_ACCESS_TOKEN")

        self.url_autorizacao = "https://auth.mercadolivre.com.br/authorization"
        self.url_token = "https://api.mercadolibre.com/oauth/token"

        if not self.client_id or not self.client_secret:
            raise RuntimeError(
                "Credenciais do Mercado Livre não configuradas no ambiente"
            )

    def gerar_url_autorizacao(self) -> str:
        """
        Gera a URL para o usuário autorizar a aplicação no Mercado Livre.
        """
        if not self.redirect_uri:
            raise RuntimeError("Redirect URI não configurado")

        return (
            f"{self.url_autorizacao}"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
        )

    def trocar_codigo_por_token(self, code: str) -> Dict:
        """
        Troca o authorization code por um access_token.

        Args:
            code: Código de autorização recebido no callback

        Returns:
            Dicionário contendo o access_token e metadados
        """
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
        }

        resposta = requests.post(self.url_token, data=payload, timeout=10)

        if resposta.status_code != 200:
            raise RuntimeError(
                f"Erro ao obter token ({resposta.status_code})"
            )

        return resposta.json()

    def obter_access_token(self) -> str:
        """
        Retorna o access_token configurado no ambiente.
        """
        if not self.access_token:
            raise RuntimeError(
                "Access token não configurado. Execute o fluxo OAuth."
            )

        return self.access_token
