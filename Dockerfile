FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

RUN pip install --no-cache-dir poetry==1.8.*   # ou a versão que você usa

COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY src/ ./src

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]