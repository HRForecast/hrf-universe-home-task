# Installation

Install packages with poetry:

    python3 -m venv venv
    . venv/bin/activate
    pip install poetry
    POETRY_VIRTUALENVS_CREATE=false poetry install

Create database:

    docker-compose up
    docker cp migrations/data/ hrf_universe_postgres:/tmp
    alembic upgrade head
