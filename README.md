# Dotum - Sistema de contas a pagar e contas a receber

[![CI](https://github.com/henriquesebastiao/dotum/actions/workflows/test.yml/badge.svg)](https://github.com/henriquesebastiao/dotum/actions/workflows/test.yml)
[![coverage](https://coverage-badge.samuelcolvin.workers.dev/henriquesebastiao/dotum.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/henriquesebastiao/dotum)
[![fastapi](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![postgresql](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

Este projeto é uma solução para um desafio de programação back-end, cujo objetivo é desenvolver uma aplicação para o controle de contas a pagar e contas a receber. A proposta foca na construção de uma lógica sólida, estrutura de código bem organizada e cumprimento dos requisitos funcionais.

### Funcionalidades

- Cadastro de contas: permite lançar contas a pagar ou a receber, com valor, descrição e data de vencimento.
- Listagem de contas: exibe todas as contas registradas, com detalhes como valor, descrição, vencimento e status (pago ou pendente).
- Total de contas a pagar: soma o valor de todas as contas a pagar pendentes.
- Total de contas a receber: soma o valor de todas as contas a receber pendentes.
- Total geral de contas: calcula o total combinando as contas a pagar e a receber.
- Autenticação de usuários com JWT (JSON Web Token).
- Criptografiia de senha com Argon2 no banco de dados.

### Tecnologias utilizadas

- Python
- FastAPI
- PostgreSQL
- Docker
- SQLAlchemy
- Pydantic
- PyTest
- GitHub Actions

### Como executar o projeto

1. Clone o repositório e entre nele com o seguinte comando:

```shell
git clone https://github.com/henriquesebastiao/dotum && cd dotum
```

2. Crie um arquivo `.env` que conterá as variáveis de ambiente exigidas pela aplicação, você pode fazer isso apenas copiando o arquivo de exemplo:

```shell
cat .env.example > .env
```

3. Agora execute o docker compose e toda aplicação será construída e iniciada em modo de desenvolvimento 🚀

```shell
docker compose up -d
```

Pronto! Você já pode abrir seu navegador e acessar as seguintes URLs:

- Documentação interativa automática com Swagger UI (do backend OpenAPI): http://localhost:9002
- Redoc, uma versão mais legível da documentação: http://localhost:9002/redoc

### Executando os testes

Para executar os testes com PyTest execute o seguinte comando:

```shell
make test
```

## Exemplos de uso da API

A seguir, alguns exemplos de requisições para consumir os principais endpoints da API do sistema de contas.

### Autenticação (Login)

```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=joao123&password=senha_segura
```

#### Resposta

```json
{
  "access_token": "seu_token_de_acesso_aqui",
  "token_type": "bearer"
}
```

### Cria usuário

```http
POST /user/
Content-Type: application/json

{
  "username": "joao123",
  "email": "joao@example.com",
  "first_name": "João",
  "last_name": "Silva",
  "password": "senha_segura"
}
```

### Cadastrar conta

```http
POST /account/
Authorization: Bearer seu_token
Content-Type: application/json

{
  "value": 200.0,
  "description": "Pagamento de fornecedor",
  "due_date": "2025-07-31",
  "account_type": "payable",
  "paid": false
}
```

### Listas contas

```http
GET /account/
Authorization: Bearer seu_token
```

### Atualizar conta

```http
PATCH /account/{account_id}
Authorization: Bearer seu_token
Content-Type: application/json

{
  "paid": true
}
```

### Deletar conta

```http
DELETE /account/{account_id}
Authorization: Bearer seu_token
```

### Total de contas a pagar

```http
GET /account/total-accounts-payable
Authorization: Bearer seu_token
```

### Total de contas a receber

```http
GET /account/total-accounts-receivable
Authorization: Bearer seu_token
```

### Total geral de contas

```http
GET /account/grand-total-of-accounts
Authorization: Bearer seu_token
```
