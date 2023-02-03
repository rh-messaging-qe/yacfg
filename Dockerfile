FROM python:3.11.1-alpine3.16 AS base

FROM base AS builder
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$PATH:/runtime/bin" \
    PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.11/site-packages"

RUN apk add --no-cache \
    build-base \
    curl \
    gcc \
    libressl-dev \
    musl-dev \
    libffi-dev \
    libzmq \
    zeromq-dev

RUN pip install --no-cache-dir --upgrade pip setuptools wheel poetry

COPY . /src
WORKDIR /src

RUN poetry build
RUN pip install --prefix=/runtime --force-reinstall dist/*.whl

FROM base AS runtime

COPY --from=builder /runtime /usr/local
RUN mkdir -p /data/output && \
  addgroup -S yacfg && \
  adduser -S -D -h /data yacfg yacfg && \
  chown -R yacfg:yacfg /data

USER yacfg
WORKDIR /data
VOLUME [ "/data/output" ]
CMD ["yacfg", "--help"]
