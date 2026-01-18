# Desafio de Programação  
## Catálogo de Produtos – API do Mercado Livre

---

## Objetivo

Desenvolver uma aplicação simples que consuma a API do Mercado Livre, incluindo o processo de autenticação, para buscar produtos ativos e exibi-los em formato de cards visuais.

Este desafio avalia:
- Capacidade de leitura de documentação técnica
- Implementação de autenticação em API REST
- Consumo e tratamento de dados reais
- Organização e clareza de código

---

## Documentação Oficial

Toda a implementação deve se basear na documentação oficial do Mercado Livre:

https://developers.mercadolivre.com.br/pt_br/api-docs-pt-br

A leitura da documentação faz parte do desafio.

---

## Autenticação (Obrigatória)

Para acessar a API utilizada neste desafio, é necessário autenticar.

Você deverá:
- Criar uma aplicação no Mercado Livre Developers
- Seguir o fluxo de autenticação descrito na documentação oficial
- Obter um access_token válido
- Utilizar esse token para autenticar as requisições à API

Observações:
- Não será fornecido passo a passo de autenticação neste documento
- O entendimento do fluxo OAuth faz parte da avaliação
- A renovação do token pode ser manual ou automática

---

## API Utilizada

Endpoint de busca de produtos:

GET https://api.mercadolibre.com/products/search

Parâmetros mínimos:
- status=active
- site_id=MLB
- q=<termo_de_busca>
- limit=10

termo_de_busca pode ser o nome do produto, ex: carregador iphone, cadeira escritório, mochila, garrafa stanley

O token de autenticação deve ser enviado conforme especificado na documentação oficial.

---

## Funcionalidades Esperadas

### 1. Busca de Produtos

- Permitir que o usuário informe um termo de busca
- Retornar até 10 produtos ativos
- Exibir mensagem adequada quando nenhum produto for encontrado

---

### 2. Tratamento dos Dados

A partir da resposta da API, exibir pelo menos as seguintes informações:

- Nome do produto
- Status
- Imagem principal (quando existir)
- Até 3 atributos relevantes (exemplo: marca, cor, capacidade)

Regras:
- Campos ausentes não devem causar erro na aplicação
- Informações inexistentes devem ser exibidas como "Não informado"

---

### 3. Cards de Produto

Cada produto deve ser exibido em um card contendo:
- Imagem do produto ou placeholder
- Nome do produto
- Lista de atributos principais
- Status do produto

O layout pode ser simples, mas deve ser organizado e legível.

---

### 4. Ordenação

Os produtos devem ser ordenados da seguinte forma:
1. Produtos que possuem imagem
2. Produtos que não possuem imagem

---

### 5. Tratamento de Erros

A aplicação deve:
- Tratar falhas de autenticação
- Tratar erros de requisição à API
- Exibir mensagens amigáveis ao usuário
- Não expor erros técnicos ou stack traces na interface

---

## Requisitos Técnicos

- Linguagem e framework de livre escolha
- Código organizado e legível
- Uso de variáveis de ambiente para segredos e tokens
- Separação básica de responsabilidades (exemplo: camada de API, camada de apresentação)

---

## Entregáveis

- Repositório Github com o código-fonte
- README contendo:
  - Instruções para rodar o projeto
  - Como configurar a autenticação
  - Breve explicação das decisões técnicas

---

## Diferenciais (Opcional)

- Renovação automática do token
- Filtro simples por atributo
- Testes automatizados básicos

---

## Critérios de Avaliação

- Autenticação funcionando corretamente
- Capacidade de ler e aplicar a documentação oficial
- Organização e clareza do código
- Tratamento adequado de erros
- Clareza na comunicação (README)