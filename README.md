# LogitrackAPI

API de logística desenvolvida com FastAPI, PostgreSQL e Redis.

## 🚀 Features

- ✅ Autenticação de usuários com hash de senha (bcrypt)
- ✅ Banco de dados PostgreSQL com SQLAlchemy Async
- ✅ Migrations versionadas com Alembic
- ✅ Cache com Redis
- ✅ Docker Compose para desenvolvimento
- ✅ Arquitetura limpa (Clean Architecture)
- ✅ Validação de dados com Pydantic
- ✅ Documentação automática (Swagger/OpenAPI)

## 📋 Pré-requisitos

- Docker e Docker Compose
- Python 3.12+ (para desenvolvimento local)
- Poetry (gerenciamento de dependências)

## 🛠️ Instalação

### Clone o repositório

```bash
git clone https://github.com/seu-usuario/logitrackapi.git
cd logitrackapi
```

### Instale as dependências

```bash
poetry install
```

## 🔧 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Nome do projeto
PROJECT_NAME=LogitrackAPI

# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/logitrack

# Redis
REDIS_URL=redis://redis:6379/0

# Segurança
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🐳 Docker Compose

### Subir os containers

```bash
docker compose up -d
```

### Verificar logs

```bash
docker compose logs -f
```

### Parar os containers

```bash
docker compose down
```

### Parar e remover volumes

```bash
docker compose down -v
```

## 🗄️ Migrations (Alembic)

Este projeto usa Alembic para versionamento do schema do banco de dados.

### Criar nova migration

```bash
docker compose run --rm api alembic revision --autogenerate -m "descrição da mudança"
```

### Aplicar migrations

```bash
docker compose run --rm api alembic upgrade head
```

### Verificar status atual

```bash
docker compose run --rm api alembic current
```

### Rollback (última migration)

```bash
docker compose run --rm api alembic downgrade -1
```

### Histórico de migrations

```bash
docker compose run --rm api alembic history
```

### Rollback para versão específica

```bash
docker compose run --rm api alembic downgrade <version_id>
```

## 🚀 Executando o Projeto

### Desenvolvimento local

```bash
# Ativar ambiente virtual
poetry shell

# Rodar a aplicação
uvicorn src.infrastructure.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker compose up -d
```

A API estará disponível em: `http://localhost:8001`

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## 🧪 Testes

### Rodar todos os testes

```bash
docker compose run --rm api pytest
```

### Rodar testes com coverage

```bash
docker compose run --rm api pytest --cov=src --cov-report=html
```

### Rodar testes específicos

```bash
docker compose run --rm api pytest tests/test_health.py -v
```

## 📁 Estrutura do Projeto

```
logitrackapi/
├── alembic/                     # Migrations do banco de dados
│   ├── versions/               # Versões das migrations
│   └── env.py
├── src/
│   ├── application/            # Camada de aplicação
│   │   ├── dtos/              # Data Transfer Objects
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── use_cases/         # Casos de uso
│   ├── core/                   # Entidades e regras de negócio
│   │   ├── entities/          # Entidades de domínio
│   │   ├── exceptions/        # Exceções customizadas
│   │   └── repositories/      # Interfaces de repositório
│   ├── infrastructure/         # Camada de infraestrutura
│   │   ├── api/               # Endpoints e routers
│   │   │   └── routers/
│   │   ├── config/            # Configurações
│   │   ├── external/          # Serviços externos
│   │   └── persistence/       # Persistência de dados
│   │       ├── database/
│   │       └── models/
│   └── shared/                 # Utilitários compartilhados
├── tests/                      # Testes automatizados
│   ├── unit/
│   └── integration/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## 🔐 Autenticação

### Criar usuário

```bash
POST http://localhost:8001/users/
Content-Type: application/json

{
  "username": "seu_usuario",
  "email": "seu@email.com",
  "password": "sua_senha"
}
```

### Login (em implementação)

```bash
POST http://localhost:8001/auth/login
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

## 📦 Dependências Principais

- **FastAPI** ^0.115.0 - Framework web
- **SQLAlchemy** ^2.0.47 - ORM com suporte async
- **Alembic** ^1.18.4 - Migrations
- **Pydantic** - Validação de dados
- **Pydantic Settings** ^2.13.1 - Gerenciamento de configurações
- **Passlib[bcrypt]** ^1.7.4 - Hash de senhas
- **Redis** ^7.2.0 - Cache
- **Uvicorn** ^0.30.0 - Servidor ASGI
- **Email Validator** ^2.1.0 - Validação de email

## 🛠️ Desenvolvimento

### Code Style

```bash
# Formatar código
poetry run black src tests

# Ordenar imports
poetry run isort src tests

# Linting
poetry run ruff check src tests

# Type checking
poetry run mypy src
```

### Pre-commit

```bash
# Instalar hooks
pre-commit install

# Rodar manualmente
pre-commit run --all-files
```

## 📝 License

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas e suporte, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.