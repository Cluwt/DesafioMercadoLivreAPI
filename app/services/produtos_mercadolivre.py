"""

César Rodrigues Ribeiro - Desafio Mercado Livre por Arthur 

Serviço de busca e processamento de produtos do Mercado Livre.

Responsável por:
- Buscar produtos ativos na API do Mercado Livre
- Tratar dados ausentes
- Ordenar produtos (com imagem primeiro)

"""

import requests
import logging
from typing import List, Dict
from urllib.parse import quote
from app.services.autenticacao_mercadolivre import AutenticacaoMercadoLivre

logger = logging.getLogger(__name__)


class ProdutosMercadoLivre:
    def __init__(self):
        self.auth = AutenticacaoMercadoLivre()
        self.base_url = "https://api.mercadolibre.com/products/search"

    def buscar_produtos(self, termo_busca: str, limit: int = 10) -> Dict:
        # Validação:
        if not termo_busca or not termo_busca.strip():
            return {
                "total": 0,
                "erro": "O termo de busca não pode estar vazio.",
                "produtos": []
            }

        # Obter token
        try:
            token = self.auth.obter_access_token()
        except Exception as e:
            return {
                "total": 0,
                "erro": str(e),
                "produtos": []
            }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "site_id": "MLB",
            "q": termo_busca.strip(),
            "limit": min(limit, 50)
        }

        try:
            logger.info(f"🔍 Fazendo requisição para: {self.base_url}")
            logger.info(f"📋 Parâmetros: {params}")
            logger.info(f"🔑 Headers: Authorization Bearer {token[:20]}...")
            
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            logger.info(f"📊 Status da resposta: {response.status_code}")
            logger.info(f"📄 Headers resposta: {dict(response.headers)}")

            if response.status_code == 401:
                logger.error("❌ Token inválido ou expirado")
                return {
                    "total": 0,
                    "erro": "Token inválido ou expirado.",
                    "produtos": []
            }

            response.raise_for_status()
            dados = response.json()
            
            logger.info(f"📦 Estrutura da resposta: {list(dados.keys())}")
            logger.info(f"📊 Total de resultados recebidos: {len(dados.get('results', []))}")

            resultados = dados.get("results", [])
            logger.info(f"🔍 Buscando produtos: '{termo_busca}' (limite: {min(limit, 50)})")
            logger.info(f"📊 Total de resultados recebidos: {len(resultados)}")
            
            # Se não encontrou resultados com /products/search, tentar com /sites/MLB/search
            if not resultados:
                logger.warning("⚠️ Nenhum resultado com /products/search, tentando fallback para /sites/MLB/search")
                fallback_url = "https://api.mercadolibre.com/sites/MLB/search"
                fallback_params = {
                    "q": termo_busca.strip(),
                    "limit": min(limit, 50)
                }
                
                try:
                    fallback_response = requests.get(
                        fallback_url,
                        headers=headers,
                        params=fallback_params,
                        timeout=10
                    )
                    
                    logger.info(f"📊 Fallback status: {fallback_response.status_code}")
                    
                    if fallback_response.status_code == 200:
                        fallback_dados = fallback_response.json()
                        fallback_results = fallback_dados.get("results", [])
                        logger.info(f"📦 Fallback encontrou {len(fallback_results)} resultados")
                        
                        if fallback_results:
                            resultados = fallback_results
                            dados = fallback_dados
                        else:
                            logger.warning("📦 Fallback também não encontrou resultados")
                    else:
                        logger.error(f"❌ Fallback falhou: {fallback_response.status_code}")
                        
                except Exception as e:
                    logger.error(f"❌ Erro no fallback: {e}")
            
            if not resultados:
                logger.warning(f"📦 Nenhum resultado encontrado para '{termo_busca}'")
                return {
                    "total": 0,
                    "erro": f"Nenhum produto encontrado para '{termo_busca}'. Verifique a ortografia ou tente termos mais genéricos (ex: 'iphone' em vez de 'iphone 17').",
                    "produtos": []
                }
            
            # Debug: verificar estrutura do primeiro resultado
            if resultados:
                primeiro_item = resultados[0]
                logger.debug(f"📋 Estrutura do primeiro item:")
                logger.debug(f"   - ID: {primeiro_item.get('id', 'N/A')}")
                logger.debug(f"   - Título: {primeiro_item.get('title', 'N/A')}")
                logger.debug(f"   - Tem thumbnail: {'Sim' if primeiro_item.get('thumbnail') else 'Não'}")
                logger.debug(f"   - Tem pictures: {'Sim' if primeiro_item.get('pictures') else 'Não'}")
            
            # A API /products/search já retorna dados básicos, vamos usar diretamente
            # sem buscar detalhes individuais para evitar 404s
            produtos = self._formatar_produtos(resultados)
            
            # Debug: verificar produtos formatados
            produtos_sem_nome = [p for p in produtos if p.get("nome") == "Não informado"]
            produtos_sem_imagem = [p for p in produtos if p.get("imagem") == "Não informado"]
            logger.info(f"Produtos formatados: {len(produtos)} total, {len(produtos_sem_nome)} sem nome, {len(produtos_sem_imagem)} sem imagem")
            
            # Debug: listar todos os status encontrados
            status_encontrados = set(p.get("status", "unknown") for p in produtos)
            logger.info(f"🔍 Status encontrados na busca: {sorted(status_encontrados)}")
            
            # Contar produtos por status
            from collections import Counter
            status_counts = Counter(p.get("status", "unknown") for p in produtos)
            logger.info(f"📊 Contagem por status: {dict(status_counts)}")

            return {
                "total": len(produtos),
                "produtos": produtos
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro de requisição: {e}")
            return {
                "total": 0,
                "erro": "Erro ao comunicar com a API do Mercado Livre.",
                "produtos": []
            }
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
            return {
                "total": 0,
                "erro": "Erro inesperado ao buscar produtos.",
                "produtos": []
            }

    def _formatar_produtos(self, resultados: List[Dict]) -> List[Dict]:
        produtos = []

        for item in resultados:
            produto_id = item.get("id")
            if not produto_id:
                logger.warning("Item sem ID encontrado, pulando...")
                continue
            
            # Extrair nome do produto - verificar vários campos possíveis
            nome = (item.get("title") or 
                   item.get("name") or 
                   item.get("product_name") or
                   "").strip()
            
            # Se ainda não tiver nome, tentar buscar novamente
            if not nome:
                logger.warning(f"Produto {produto_id} sem nome após formatação, tentando buscar novamente...")
                # Não buscar aqui para evitar loop, apenas logar
                nome = "Não informado"
            
            # Extrair imagem - tentar várias fontes
            imagem = self._extrair_imagem(item)
            
            # Log se ainda estiver sem dados
            if nome == "Não informado" or imagem == "Não informado":
                logger.warning(f"Produto {produto_id} ainda sem dados completos - nome: {nome != 'Não informado'}, imagem: {imagem != 'Não informado'}")
            
            # Extrair URL do produto (permalink)
            # Preferir permalink do anúncio (página de venda) quando disponível
            buy_box = item.get("buy_box_winner") if isinstance(item.get("buy_box_winner"), dict) else {}
            permalink_venda = buy_box.get("permalink")
            permalink = permalink_venda or item.get("permalink") or item.get("url") or item.get("product_url")
            if permalink and str(permalink).strip().startswith("http"):
                url_produto = str(permalink).strip()
            else:
                url_produto = "Não informado"
            
            # Extrair preço se disponível
            preco = None
            try:
                if item.get("price"):
                    preco = float(item.get("price"))
                elif item.get("prices") and len(item.get("prices", [])) > 0:
                    preco_valor = item.get("prices")[0].get("amount")
                    if preco_valor:
                        preco = float(preco_valor)
            except (ValueError, TypeError):
                preco = None

            status = item.get("status")
            if not status or not str(status).strip():
                status = "unknown"
            else:
                status = str(status).strip().lower()
            
            # Não sobrescrever status para inactive - produtos já vêm como active da API
            # if item.get("_detalhes_status") == 404:
            #     status = "inactive"
            #     logger.debug(f"Produto {produto_id} marcado como inactive devido a 404 no detalhe do anúncio")

            produtos.append({
                "id": produto_id,
                "nome": nome,
                "status": status,
                "imagem": imagem,
                "url": url_produto,
                "preco": preco,
                "atributos": self._extrair_atributos(item)
            })

        # Ordenar: com imagem primeiro
        produtos.sort(key=lambda p: p["imagem"] == "Não informado")

        return produtos
    
    def _buscar_detalhes_produto(self, produto_id: str, token: str) -> Dict:
        
        try:
            url = f"https://api.mercadolibre.com/items/{produto_id}"
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers, timeout=5)  # Timeout menor para não travar
            
            if response.status_code == 200:
                dados = response.json()
                title = dados.get('title', '').strip()
                thumbnail = dados.get('thumbnail') or dados.get('secure_thumbnail') or ''
                has_pictures = bool(dados.get('pictures') and len(dados.get('pictures', [])) > 0)
                
                logger.debug(f"Detalhes obtidos para {produto_id}: title={bool(title)}, thumbnail={bool(thumbnail)}, pictures={has_pictures}")
                
                if not title:
                    logger.warning(f"Produto {produto_id} retornado sem title do endpoint /items")
                if not thumbnail and not has_pictures:
                    logger.warning(f"Produto {produto_id} retornado sem thumbnail/pictures do endpoint /items")
                
                return {"_http_status": 200, **dados}
            elif response.status_code == 404:
                # 404 é comum - produto pode não existir mais ou não estar acessível
                logger.debug(f"Produto {produto_id} não encontrado (404) - pode ter sido removido")
                return {"_http_status": 404}
            elif response.status_code == 401:
                logger.error(f"Token inválido ao buscar detalhes de {produto_id}")
                return {"_http_status": 401}
            else:
                logger.debug(f"Erro ao buscar detalhes para {produto_id}: status {response.status_code}")
                return {"_http_status": response.status_code}
        except requests.exceptions.Timeout:
            logger.debug(f"Timeout ao buscar detalhes para {produto_id}")
            return {"_http_status": 408}
        except requests.exceptions.RequestException as e:
            logger.debug(f"Erro de requisição ao buscar detalhes para {produto_id}: {str(e)}")
            return {"_http_status": 503}
        except Exception as e:
            logger.error(f"Exceção inesperada ao buscar detalhes para {produto_id}: {str(e)}")
        return {"_http_status": 500}
    
    def _extrair_imagem(self, produto: Dict) -> str:
        """Extrai a URL da imagem do produto, tentando várias fontes."""
        # Tentar secure_thumbnail primeiro (HTTPS)
        imagem = produto.get("secure_thumbnail")
        if imagem and imagem.strip():
            return imagem.strip()
        
        # Tentar thumbnail
        imagem = produto.get("thumbnail")
        if imagem and imagem.strip():
            imagem = imagem.strip()
            # Converter HTTP para HTTPS se necessário
            if imagem.startswith("http://"):
                imagem = imagem.replace("http://", "https://", 1)
            return imagem
        
        # Tentar pegar a primeira imagem de pictures
        pictures = produto.get("pictures", [])
        if pictures and len(pictures) > 0:
            primeira_imagem = pictures[0]
            if isinstance(primeira_imagem, dict):
                # Preferir secure_url
                imagem = primeira_imagem.get("secure_url") or primeira_imagem.get("url")
                if imagem and imagem.strip():
                    imagem = imagem.strip()
                    # Converter HTTP para HTTPS se necessário
                    if imagem.startswith("http://"):
                        imagem = imagem.replace("http://", "https://", 1)
                    return imagem
            elif isinstance(primeira_imagem, str):
                # Se pictures for uma lista de strings
                imagem = primeira_imagem.strip()
                if imagem.startswith("http://"):
                    imagem = imagem.replace("http://", "https://", 1)
                return imagem
        
        return "Não informado"

    def _extrair_atributos(self, produto: Dict, max_atributos: int = 3) -> List[Dict]:
        atributos_formatados = []

        atributos = produto.get("attributes", [])

        for attr in atributos[:max_atributos]:
            nome = attr.get("name")
            valor = attr.get("value_name")

            if nome and valor:
                atributos_formatados.append({
                    "nome": nome,
                    "valor": valor
                })

        while len(atributos_formatados) < max_atributos:
            atributos_formatados.append({
                "nome": "Não informado",
                "valor": "Não informado"
            })

        return atributos_formatados
