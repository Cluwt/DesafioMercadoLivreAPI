# 🧪 Testes de Tratamento de Erros

Esta pasta contém 5 testes específicos para validar o tratamento de erros da aplicação.

## 📋 Lista de Testes

### 1. `test_erro_autenticacao.py`
**Objetivo:** Testar falhas de autenticação
- ✅ Token inválido
- ✅ Sem token
- ✅ Token expirado

### 2. `test_erro_requisicao.py`
**Objetivo:** Testar erros de requisição à API
- ✅ Timeout
- ✅ Conexão recusada
- ✅ Parâmetros inválidos
- ✅ Método não permitido

### 3. `test_mensagens_amigaveis.py`
**Objetivo:** Verificar mensagens amigáveis ao usuário
- ✅ Erro genérico
- ✅ Busca vazia
- ✅ Limite excedido

### 4. `test_sem_exposicao_tecnica.py`
**Objetivo:** Garantir que não expõe erros técnicos
- ✅ Respostas JSON
- ✅ Página HTML
- ✅ Headers de resposta

### 5. `test_interface_erros.py`
**Objetivo:** Testar interface de tratamento de erros
- ✅ Busca sem resultados
- ✅ Caracteres especiais
- ✅ Termo muito longo
- ✅ Múltiplas requisições

## 🚀 Como Executar

### Executar todos os testes:
```cmd
RODAR_TODOS.bat
```

### Executar teste individual:
```cmd
python test_erro_autenticacao.py
python test_erro_requisicao.py
python test_mensagens_amigaveis.py
python test_sem_exposicao_tecnica.py
python test_interface_erros.py
```

## 📋 Pré-requisitos

1. **Servidor rodando:** `python -m uvicorn app.main:app --port 8000`
2. **Python 3.7+** com bibliotecas instaladas
3. **Acesso à internet** para testes de API

## 🎯 Critérios de Sucesso

### ✅ Falha de Autenticação
- Retorna erro 401 para token inválido
- Mensagem amigável sem expor credenciais
- Trata token expirado corretamente

### ✅ Erros de Requisição
- Trata timeout sem crashar
- Lida com conexões recusadas
- Valida parâmetros adequadamente
- Retorna método não permitido (405)

### ✅ Mensagens Amigáveis
- Sem termos técnicos (Exception, Traceback)
- Linguagem construtiva ("tente", "por favor")
- Explica o problema claramente

### ✅ Sem Exposição Técnica
- Nenhum stack trace na resposta
- Sem detalhes de implementação
- Headers seguros (sem Server, X-Debug)

### ✅ Interface de Erros
- Trata casos extremos (termos longos, especiais)
- Lida com múltiplas requisições
- Mantém usabilidade em caso de erro

## 📊 Relatório de Testes

Após executar, verifique:

- **✅ Passou:** Teste bem-sucedido
- **❌ Falhou:** Precisa correção
- **⚠️ Aviso:** Funciona mas pode melhorar

## 🔧 Correções Sugeridas

Se algum teste falhar, verifique:

1. **Handlers de exceção** na API
2. **Mensagens de erro** nos endpoints
3. **Headers de resposta** no FastAPI
4. **Tratamento no frontend** (JavaScript)
5. **Logging** (não deve expor para usuário)

## 📝 Notas

- Testes devem ser executados com o servidor rodando
- Alguns testes podem demorar (timeout, múltiplas requisições)
- Resultados são exibidos no console
- Testes não modificam dados permanentemente
