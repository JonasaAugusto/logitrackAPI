# LogitrackAPI

API REST de rastreamento logístico construída com **FastAPI**, seguindo os princípios de **Clean Architecture**. Desenvolvida como projeto de portfólio para demonstrar boas práticas em Python backend: autenticação robusta, cache, resiliência e observabilidade.

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Framework | FastAPI + Uvicorn |
| Banco de dados | PostgreSQL 15 (async via psycopg3) |
| ORM | SQLAlchemy 2 (async) |
| Migrations | Alembic |
| Cache / Sessões | Redis 7 |
| Autenticação | JWT (python-jose) + Bcrypt |
| Logs | Structlog |
| Testes | pytest-asyncio + httpx |
| Qualidade | ruff + black + isort + mypy + pre-commit |
| Infra | Docker Compose |
| CI/CD | GitHub Actions |

---

## Arquitetura

```
src/
├── core/                        # Domínio puro (sem dependências externas)
│   ├── entities/                # Entidades de negócio (dataclasses)
│   ├── repositories/            # Interfaces (ABC)
│   └── exceptions/              # Exceções de domínio
├── application/                 # Casos de uso e DTOs
│   ├── use_cases/               # CreateUser, AuthenticateUser, etc.
│   └── dtos/                    # Pydantic schemas (entrada/saída)
└── infrastructure/              # Implementações concretas
    ├── api/
    │   ├── routers/             # auth, users, deliveries, tracking
    │   ├── middleware/          # Rate limiting (Redis)
    │   └── background/          # Webhook assíncrono (asyncio)
    ├── config/                  # JWT, settings, logging
    ├── cache.py                 # Cliente Redis
    └── persistence/
        ├── models/              # SQLAlchemy ORM (User, Vehicle, Delivery, TrackingEvent)
        ├── repositories/        # Implementações de IUserRepository
        └── database/            # Engine async, sessão, Base
```

> A dependência flui sempre de fora para dentro: `infrastructure → application → core`. O `core` não conhece FastAPI, SQLAlchemy ou Redis.

---

## Funcionalidades

### Autenticação
- Registro e login com hash Bcrypt
- Access Token (30 min) + Refresh Token (7 dias)
- Revogação de Refresh Token via Redis
- Logout com invalidação imediata

### Usuários
- CRUD completo com paginação (`skip` / `limit`)
- Cache de `GET /users/{id}` no Redis (TTL 5 min, invalidado no PATCH/DELETE)

### Entregas
- CRUD de veículos (caminhão, van, moto, carro)
- Criação de entregas com código de rastreio gerado automaticamente (`LT` + 10 chars)
- Histórico de eventos automático a cada mudança de status
- **Idempotência**: `POST /deliveries/` aceita `X-Idempotency-Key` — requisições duplicadas retornam o mesmo resultado sem criar duplicatas (chave armazenada no Redis por 24h)
- **Webhook assíncrono**: após cada criação de entrega, um background job simula o dispatch de webhook sem bloquear a resposta

### Resiliência
- Rate limiting: 100 req/min por IP via Redis (falha silenciosa se Redis indisponível)
- CORS configurado por origens permitidas

### Observabilidade
- `GET /health` — verifica conectividade com PostgreSQL e Redis
- `GET /metrics` — contagens de usuários, entregas por status e veículos
- Logs estruturados com Structlog (JSON-ready)

---

## Como executar

### Pré-requisitos
- Docker e Docker Compose
- (Opcional) Python 3.12 + Poetry para desenvolvimento local

### 1. Subir o ambiente

```bash
git clone https://github.com/JonasaAugusto/logitrackAPI.git
cd logitrackAPI
cp .env.example .env        # ajuste as variáveis se necessário
docker compose up -d --build
```

### 2. Aplicar migrations

```bash
docker compose exec api alembic upgrade head
```

### 3. Acessar a documentação

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redocs

---

## Endpoints

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Cadastrar usuário |
| POST | `/auth/login` | Login (form data) — retorna access + refresh token |
| POST | `/auth/refresh` | Renovar tokens com refresh token |
| POST | `/auth/logout` | Revogar refresh token |

### Usuários (requer JWT)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/users/` | Listar usuários (paginado) |
| GET | `/users/{id}` | Buscar usuário (com cache Redis) |
| PATCH | `/users/{id}` | Atualizar usuário |
| DELETE | `/users/{id}` | Remover usuário |

### Veículos (requer JWT)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/vehicles/` | Cadastrar veículo |
| GET | `/vehicles/` | Listar veículos |
| GET | `/vehicles/{id}` | Buscar veículo |

### Entregas (requer JWT)
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/deliveries/` | Criar entrega (`X-Idempotency-Key` opcional) |
| GET | `/deliveries/` | Listar entregas com histórico de eventos |
| GET | `/deliveries/{tracking_code}` | Buscar entrega por código |
| PATCH | `/deliveries/{tracking_code}` | Atualizar status (gera evento automático) |

### Sistema
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Status de DB e Redis |
| GET | `/metrics` | Contagens agregadas |

---

## Variáveis de ambiente

```env
DATABASE_URL=postgresql+psycopg://user:password@db:5432/logitrack
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=sua-chave-secreta-aqui
EXTERNAL_API_KEY=chave-api-externa
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## Testes

```bash
# Com Docker
docker compose exec api pytest -v

# Local (com Poetry)
poetry run pytest -v
```

A suíte cobre validação de DTOs, entidades de domínio, endpoints E2E com mocks de DB e Redis, autenticação, fluxos de delivery e health checks.

---

## CI/CD

Pipeline no GitHub Actions (`.github/workflows/ci.yml`) que executa em todo push para `main`:

1. Sobe PostgreSQL 15 e Redis 7 como services
2. Instala dependências via Poetry
3. Aplica migrations com Alembic
4. Executa `pytest` + `mypy`

---

## Licença

MIT — veja `LICENSE` para detalhes.
