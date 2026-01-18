# Como Executar com Docker

## Pré-requisitos
- Docker instalado na máquina
- Docker Compose instalado
- Token Ngrok (opcional, para exposição pública)

## Passos para Executar

### 1. Configurar Ngrok (Opcional)
Se precisar expor publicamente:
```bash
# Adicione ao arquivo .env:
NGROK_AUTHTOKEN=seu_token_aqui
```

### 2. Construir e Iniciar a Aplicação
```bash
docker-compose up --build
```

### 3. Acessar a Aplicação
- **Local**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/saude
- **Ngrok Interface**: http://localhost:4040 (se ativado)

### 4. Parar a Aplicação
```bash
docker-compose down
```

## Comandos Úteis

### Ver logs em tempo real
```bash
docker-compose logs -f
```

### Ver logs específicos
```bash
docker-compose logs -f app      # Apenas aplicação
docker-compose logs -f ngrok    # Apenas ngrok
```

### Reconstruir imagem
```bash
docker-compose build --no-cache
```

### Executar em background
```bash
docker-compose up -d
```

## Variáveis de Ambiente
Configure as variáveis no arquivo `.env`:
- `CLIENT_ID` - ID do cliente Mercado Livre
- `CLIENT_SECRET` - Secret do cliente Mercado Livre
- `REDIRECT_URI` - URL de redirecionamento OAuth
- `NGROK_AUTHTOKEN` - Token do ngrok (opcional)

## Portas
- **8000**: Aplicação FastAPI
- **4040**: Interface Ngrok (se ativado)

## Estrutura Docker
- **Dockerfile**: Configuração do container Python
- **docker-compose.yml**: Orquestração com app + ngrok
- **.dockerignore**: Arquivos ignorados no build

## Troubleshooting

### Ngrok Offline
Se aparecer `ERR_NGROK_3200`:
1. Verifique se `NGROK_AUTHTOKEN` está configurado
2. Aguarde alguns segundos para o túnel estabilizar
3. Acesse http://localhost:4040 para status do ngrok

### Recriar containers
```bash
docker-compose down
docker-compose up --build
```
