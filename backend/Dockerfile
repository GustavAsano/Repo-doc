FROM python:3.10-slim-bookworm

ARG USER=ubuntu
ARG UID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_DATA_DIR=/app/data

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libssl-dev \
    pkg-config \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --uid ${UID} ${USER}

# Create app and data dirs with correct ownership before switching user
USER root
RUN mkdir -p \
      /app/data/in \
      /app/data/out \
      /app/data/workspace \
      /app/data/library/repos \
      /app/data/library_functional/repos \
      /app/data/.chat_history && \
    chown -R ${UID}:${UID} /app /app/data
USER ${UID}

WORKDIR /app

RUN pip3 install "uv>=0.4.12" --user
ENV PATH="/home/${USER}/.local/bin:${PATH}"
ENV UV_PROJECT_ENVIRONMENT="/home/${USER}/.venv"

COPY --chown=${UID}:${UID} pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --no-editable

COPY --chown=${UID}:${UID} . .
RUN uv sync --no-dev

EXPOSE 8000