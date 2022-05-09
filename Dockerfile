FROM python:3.9-buster

WORKDIR /app

ENV PYTHONPATH=/app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock & pyproject.toml
COPY ./backend/poetry.lock /app/
COPY ./backend/pyproject.toml /app/

# Install dependencies
RUN bash -c "poetry install --no-root --no-dev"

# Copy source files
COPY ./backend /app
COPY ./frontend/index.html /app/index.html
COPY ./frontend/style.css /app/style.css

# Start the service
CMD [ "python", "main.py"]
