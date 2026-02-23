# LogitrackAPI

API de logística desenvolvida em **FastAPI**, com persistência em **PostgreSQL** e infraestrutura via **Docker Compose**. Este projeto faz parte de um estudo acadêmico e segue boas práticas de arquitetura limpa e versionamento com GitHub.

---

## 🚀 Tecnologias
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)

- [FastAPI](https://fastapi.tiangolo.com/) — framework web moderno e rápido
- [PostgreSQL](https://www.postgresql.org/) — banco de dados relacional
- [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) — containers e orquestração
- [Poetry](https://python-poetry.org/) — gerenciamento de dependências e ambientes virtuais

---

## 📂 Estrutura do projeto

```
logitrackAPI/
├── api/ # Código principal da aplicação FastAPI
├── tests/ # Testes automatizados
├── docker-compose.yml
├── pyproject.toml # Configuração do Poetry
└── README.md
```

---

## ⚙️ Instalação e execução

### 1. Clonar o repositório

```bash
git clone git@github.com:JonasaAugusto/logitrackAPI.git
cd logitrackAPI
```

### 2. Instalar dependências com Poetry

```bash
poetry install
```

### 3. Rodar localmente com Docker Compose

```bash
docker compose up --build
```

A API estará disponível em:

👉 `http://localhost:8000`

### 🧪 Testes

Para rodar os testes:

```bash
poetry run pytest
```

---

## 📌 Próximos passos

- Configurar CI/CD com GitHub Actions (lint + testes automáticos).
- Adicionar Redis para cache e filas.
- Documentar endpoints com OpenAPI/Swagger (já integrado ao FastAPI).

---

## 📄 Licença

Este projeto é de uso acadêmico e está sob a licença MIT.


