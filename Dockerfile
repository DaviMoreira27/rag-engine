FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir pipx && \
    pipx install poetry && \
    pipx ensurepath

ENV PATH="/root/.local/bin:$PATH"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --without dev

COPY . .

FROM python:3.13-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY --from=builder /app/app app

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
