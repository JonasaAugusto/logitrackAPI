FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY src/ ./src

CMD ["uvicorn", "infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]