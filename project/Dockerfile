# Base Image
###############################################
FROM python:3.10-slim as python-base

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    PYTHONPATH="/usr/src/app"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder Image
###############################################
FROM python-base as builder-base

# install system dependencies
RUN apt-get update && apt-get install -y  \
    build-essential \
    curl  \
    netcat  \
    gcc \
    postgresql \
    && rm -rf /var/lib/apt/lists/*

# install poetry
ENV POETRY_VERSION=1.2.0a2
RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-root

# Development Image
###############################################
FROM builder-base as development

# create the app user
RUN addgroup --system app && adduser --system --group app

WORKDIR /usr/src/app

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod 755 /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

