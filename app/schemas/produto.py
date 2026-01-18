"""
Schemas Pydantic para validação e serialização de dados.

Define os modelos de dados utilizados na API para garantir
validação e documentação automática.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class Atributo(BaseModel):
    """Modelo para atributos de um produto."""
    nome: str = Field(..., description="Nome do atributo (ex: Marca, Cor)")
    valor: str = Field(..., description="Valor do atributo")


class Produto(BaseModel):
    """Modelo completo de um produto."""
    id: str = Field(..., description="ID único do produto")
    nome: str = Field(..., description="Nome do produto")
    status: str = Field(..., description="Status do produto (ex: active)")
    imagem: str = Field(..., description="URL da imagem principal ou 'Não informado'")
    url: Optional[str] = Field(None, description="URL do produto no Mercado Livre")
    preco: Optional[float] = Field(None, description="Preço do produto")
    atributos: List[Atributo] = Field(..., description="Lista de até 3 atributos principais")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "MLB123456789",
                "nome": "Carregador iPhone 15 Pro Max",
                "status": "active",
                "imagem": "https://http2.mlstatic.com/D_123456.jpg",
                "atributos": [
                    {"nome": "Marca", "valor": "Apple"},
                    {"nome": "Cor", "valor": "Branco"},
                    {"nome": "Capacidade", "valor": "20W"}
                ]
            }
        }


class RespostaBusca(BaseModel):
    """Modelo de resposta da busca de produtos."""
    total: int = Field(..., description="Número total de produtos encontrados", ge=0)
    produtos: List[Produto] = Field(..., description="Lista de produtos encontrados")
    erro: Optional[str] = Field(None, description="Mensagem de erro, se houver")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 5,
                "produtos": [],
                "erro": None
            }
        }
