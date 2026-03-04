# LogitrackAPI

API robusta de logística desenvolvida sob os princípios de **Clean Architecture**, focada em alta performance e escalabilidade para gestão de usuários e rastreamento de encomendas.

---

## 🚀 Funcionalidades Implementadas

* **Autenticação JWT**: Segurança avançada com OAuth2, tokens Bearer e hash de senhas via Bcrypt.
* **CRUD de Usuários**: Gestão completa de usuários (Create, Read, Update, Delete) com validação rigorosa via Pydantic DTOs.
* **Rastreio de Encomendas**: Sistema de consulta de status com integração para APIs externas (ex: Correios).
* **Infraestrutura Moderna**: Persistência assíncrona com PostgreSQL/SQLAlchemy e cache resiliente com Redis.
* **Dockerizado**: Ambiente isolado garantindo paridade entre desenvolvimento e produção.

---

## 🏗️ Estrutura do Projeto

O projeto é organizado em camadas para garantir o desacoplamento:

* `src/core`: Entidades e regras de negócio puras.
* `src/application`: Casos de uso e Data Transfer Objects (DTOs).
* `src/infrastructure`: Implementações de API, Banco de Dados e integrações externas.

---

## 🛠️ Instalação e Execução

### 1. Preparação

```bash
git clone https://github.com/seu-usuario/logitrackapi.git
cd logitrackapi
cp .env.example .env

```

### 2. Levantando o Ambiente

```bash
docker compose up -d --build

```

### 3. Banco de Dados (Migrations)

```bash
docker compose exec api alembic upgrade head

```

---

## 📮 Testando com Postman

A API foi validada e está pronta para consumo via Postman. A coleção de endpoints está organizada da seguinte forma:

* **Login**: Endpoint para autenticação e geração de token JWT.
* **CRUD**: Operações completas de usuários (POST, GET, PATCH, DELETE).
* **API**: Endpoint de rastreio (`GET TrackingAPI`) para consulta de encomendas.
* **ConnectionTest**: Verificação de integridade da API, Redis e DB.

---

## 📚 Documentação Automática

Com o container ativo, acesse:

* **Swagger UI**: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)

---

## 🧪 Suíte de Testes

Os testes automatizados garantem a estabilidade do CRUD e das integrações:

```bash
docker compose exec api pytest -v

```

---

## 📝 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

**Status do Projeto**: 🚀 Pronto para Integração Front-end.