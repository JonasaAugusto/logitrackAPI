FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --only main

COPY src/ ./src

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.infrastructure.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
