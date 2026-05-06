FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /code/

RUN poetry lock
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /code/

CMD ["python", "run.py"]