# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    swift

RUN python -m pip install poetry

WORKDIR /backend-app/

COPY . .

WORKDIR /backend-app/app/

#Installing project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

#USER swift

EXPOSE 5000

RUN chmod +x ./scripts/* 

ENTRYPOINT ./scripts/docker-entrypoint-backend.sh
