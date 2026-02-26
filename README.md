# LogitrackAPI

API de logística desenvolvida em **FastAPI**, com persistência em **PostgreSQL**, cache em **Redis** e infraestrutura containerizada via **Docker Compose**. Este projeto faz parte de um estudo acadêmico e segue boas práticas de arquitetura limpa, validação de dados e integração contínua (CI/CD).

---

## 🚀 Status do Projeto (Dia 3)

- [x] **CI/CD:** Pipeline configurado com Lint, Testes e Build (GitHub Actions).
- [x] **Docker:** API, PostgreSQL e Redis integrados e operacionais.
- [x] **Core:** Entidade `User` criada com validação Pydantic e DTOs separados.
- [x] **Rotas:** Router de usuários implementado com Type Hints.
- [x] **Health Check:** Monitoramento de conexão com DB e Redis.

---

## 🛠 Tecnologias

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-black?logo=github-actions)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)

- [FastAPI](https://fastapi.tiangolo.com/) — framework web moderno e rápido
- [PostgreSQL](https://www.postgresql.org/) — banco de dados relacional
- [Redis](https://redis.io/) — cache e gerenciamento de estado
- [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) — containers e orquestração
- [Poetry](https://python-poetry.org/) — gerenciamento de dependências
- [GitHub Actions](https://github.com/features/actions) — automação de CI/CD

---

## 📂 Estrutura do Projeto

```plaintext
logitrackAPI/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de CI/CD
├── src/
│   ├── infrastructure/     # Implementação de DB, API, Routers
│   ├── core/               # Entidades de Domínio
│   └── application/        # Casos de uso e DTOs
├── tests/                  # Testes automatizados
├── docker-compose.yml      # Orquestração (API + Postgres + Redis)
├── pyproject.toml          # Configuração do Poetry
└── README.md
```


---

## ⚙️ Instalação e Execução

### 1. Clonar o repositório

```bash
git clone git@github.com:JonasaAugusto/logitrackAPI.git
cd logitrackAPI
```

### 2. Rodar com Docker Compose (Recomendado)
Este comando sobe a API, o banco de dados PostgreSQL e o Redis simultaneamente

```bash
docker compose up --build
```


A API estará disponível em:
👉 http://localhost:8001
👉 Swagger Docs: `http://localhost:8001/docs`

### 3. Desenvolvimento Local (Opcional)
Se preferir rodar sem Docker para desenvolvimento:

```bash
poetry install
poetry run uvicorn infrastructure.api.main:app --reload
```

## 🧪 Testes
Para rodar a suíte de testes automatizados:

```bash
poetry run pytest
```

## 📚 Documentação da API (Endpoints Principais)
A documentação interativa está disponível em `/docs`. Abaixo, exemplos de requisições e respostas testadas.

### 1. 🏠 Root & Health Check
Verifica se o servidor e as conexões (DB/Redis) estão saudáveis.

**GET** `/`
```json
{
  "message": "Server is running!"
}
```

**GET** `/health`
```json
{
  "status": "ok",
  "database": "connected",
  "redis": "connected"
}
```

### 2. 👥 Usuários
**POST** `/users/` (Criar Usuário)

*Request:*
```json
{
  "username": "jonas_dev",
  "email": "jonas@example.com",
  "password": "senha123"
}
```

*Response (201 Created):*
```json
{
  "id": 1,
  "username": "jonas_dev",
  "email": "jonas@example.com",
  "is_active": true,
  "created_at": "2026-02-25T23:22:05.522726"
}
```

### 3. 📦 Tracking (Placeholder)
**GET** `/tracking/`

*Response:*
```json
{
  "message": "Tracking endpoint placeholder"
}
```

## 📌 Próximos Passos
- [ ] Implementar Autenticação e Autorização (JWT OAuth2).
- [ ] Desenvolver CRUD completo de Entregas e Tracking.
- [ ] Integrar testes de integração no pipeline CI/CD.
- [ ] Criar frontend simples para consumo da API.

## 📄 Licença
Este projeto é de uso acadêmico e está sob a licença MIT.
```