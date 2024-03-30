FROM python:3.11-slim as base

#EXPOSE 8080

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
#ARG REQUIREMENTS_DEV=False

WORKDIR /app

FROM base as builder

ENV PIP_NO_CACHE_DIR=1

COPY requirements.txt .
COPY requirements-dev.txt .

RUN apt-get update &&  \
    apt-get install libffi-dev libpq-dev liblz4-dev libunwind-dev -y \
    && apt-get clean\
    && pip install -U pip \
    && pip install -r requirements.txt

RUN if "$REQUIREMENTS_DEV" ; then pip install -r /requirements.dev.txt ; fi

COPY ./src /app/src/
COPY ./alembic.ini /app/alembic.ini
COPY ./migration /app/migration
COPY ./tests /app/tests/

FROM base as final

RUN groupadd -r -g 1000 app_group && useradd -r -g app_group -u 1000 app_user
RUN chown -R app_user:app_group /app
USER app_user

CMD ["uvicorn", "src.main:app", "--workers", "4", "--host", "0.0.0.0", "--port", "8000"]
