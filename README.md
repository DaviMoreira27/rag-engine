# rag-engine

Multi-tenant RAG backend. Users belong to organizations and can create multiple RAG instances per org, each with its own uploaded documents, access controls, and chat sessions.

## Overview

Each RAG instance is scoped to an organization. Members can be granted access to one or more RAGs, either as readers (query-only) or with broader chat history access. File ingestion, embedding, and retrieval are handled per-RAG-instance, with vector storage backed by pgvector.

## Stack

| Concern | Technology |
|---|---|
| API | FastAPI + Pydantic |
| ORM | SQLAlchemy |
| RAG / LLM orchestration | LangChain |
| LLM providers | OpenAI, Claude, Bedrock |
| Embeddings | gemini-embedding-001 |
| Vector store | pgvector |
| Persistence | PostgreSQL |
| Cache + session | Redis |
| Object storage | S3 |
| Scraping | Playwright |
| Messaging / streaming | Kafka |
| Notifications | SNS + SQS + DynamoDB |
| Observability | OTel SDK + Loki + Prometheus + Grafana |
| LLM observability | Langfuse |
| Auth | JWT (custom) |
| Infra | K8s on EC2 (see [rag-infrastructure](https://github.com/DaviMoreira27/rag-infrastructure)) |

## Running locally

**Requirements:** Python 3.13, [pipx](https://pipx.pypa.io/stable/installation/), [Poetry](https://python-poetry.org/docs/), Docker

```sh
# Install dependencies
poetry install

# Start PostgreSQL and Redis
docker run -d --name rag-postgres --env-file .env -p 5432:5432 postgres:16-alpine
docker run -d --name rag-redis --env-file .env -p 6379:6379 redis:7-alpine

# Run migrations
poetry run task migrate

# Start dev server
poetry run task dev
```

**Available tasks:**

```sh
poetry run task dev              # start uvicorn dev server
poetry run task test             # run all tests
poetry run task test-unit        # run unit tests
poetry run task test-integration # run integration tests
poetry run task migrate          # apply migrations
poetry run task migration <msg>  # generate a new migration
```

## Planned features

- Multi-tenant RAG management (per-org RAG instances with isolated document stores)
- File upload and ingestion pipeline (chunking, embedding, indexing)
- Web scraping as a document source
- Per-RAG access control (query-only vs. full chat history)
- Multi-model support (OpenAI, Claude, Bedrock) configurable per RAG
- Redis-backed session management and request caching, isolated in separate databases (db0: cache, db1: sessions)
- Async notifications via SNS + SQS + DynamoDB
- Full observability stack: traces (OTel), metrics (Prometheus), logs (Loki), dashboards (Grafana)
- LLM-level tracing and evaluation via Langfuse
- Kafka-based streaming for long-running ingestion jobs
- K8s deployment on EC2 (infra defined in [rag-infrastructure](https://github.com/DaviMoreira27/rag-infrastructure))


**1. Modelar `RAGInstance`**
Model + migration. Campos: `rag_id`, `tenant_id` (FK), `name`, `llm_provider`, `llm_model`, configurações de chunking. É a entidade central de tudo que vem depois.

**2. Modelar `RAGMember` (access control)** -- TenantMember, the access control must be perfomed on the entirety of the organization
Tabela de relação `user_id` + `rag_id` + `role` (query-only | full). Sem isso não tem como proteger nenhum endpoint de RAG.

**3. CRUD de RAG**
Endpoints para criar, listar e deletar RAGs de um tenant. Dependency que valida se o usuário tem acesso ao RAG antes de qualquer operação.

**4. Migrar vector store para pgvector**
Trocar Chroma local por pgvector. A collection precisa ser isolada por `rag_id`. Habilitar extensão no Postgres, ajustar o `RagEngine`.

**5. File upload**
Receber arquivo via multipart, fazer upload para S3 com path `{tenant_id}/{rag_id}/{filename}`, retornar referência.

**6. Ingestion pipeline (síncrona primeiro)**
Ler arquivo do S3, chunking, embedding, indexar no pgvector no contexto do `rag_id` correto. Depois de funcionar, migrar para assíncrono.

**7. Web scraper**
Mesma pipeline de ingestion, mas a entrada é uma URL. Implementar o router e reusar o pipeline.

**8. Endpoint de query**
Receber pergunta, fazer retrieval no pgvector filtrando por `rag_id`, montar prompt, chamar LLM, retornar resposta.

**9. Histórico de chat**
Modelar `ChatSession` e `ChatMessage` no Postgres. Persistir pergunta + resposta a cada query. Listar histórico por sessão.

**10. Kafka: ingestion assíncrona**
Transformar upload de arquivo em evento (`file.uploaded`). Consumer processa ingestion em background. Necessário antes de escalar.

**11. Notificações (SNS + SQS + DynamoDB)**
Ao fim da ingestion (sucesso ou erro), publicar no SNS. DynamoDB guarda histórico de notificações por usuário.

**12. Instrumentação OTel**
Adicionar traces nas operações críticas: query, ingestion, upload, auth. Exportar para Loki e Prometheus.

**13. Langfuse**
Rastrear todas as chamadas LLM: tokens, latência, modelo usado, custo estimado.

**14. Grafana**
Dashboards de latência, erros, throughput por tenant/RAG, uso de tokens.

**15. Testes**
Unitários nos services, integração com banco real e Redis, contrato nos endpoints HTTP.

**16. Docker + K8s + CI/CD**
Revisar Dockerfile, escrever manifests K8s, configurar pipeline de build/deploy no `rag-infrastructure`.
