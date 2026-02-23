PYTHON_VERSION=3.14.3

setup:
    pyenv local $(PYTHON_VERSION)
    poetry install

shell:
    poetry shell

run:
    poetry run uvicorn src.logitrackapi.main:app --reload

test:
    poetry run pytest

docker-up:
    docker-compose up -d

docker-down:
    docker-compose down

health:
    curl http://localhost:8000/health
