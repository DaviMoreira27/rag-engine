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
