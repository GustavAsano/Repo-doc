FROM python:3.10-slim-bookworm
ARG USER=ubuntu
ARG UID=1000
ARG SSH_PRIVATE_KEY
ARG SSH_CONFIG

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libssl-dev \
    libzmq3-dev \
    pkg-config \
    wget \
    pipx

# Create a non-root user with uid and gid of current user (host)
RUN adduser --disabled-password --uid ${UID} ${USER} --home /home/${USER}
WORKDIR /app
RUN chown -R ${UID}:${UID} /app

# Set the user
USER ${UID}

# Install uv
RUN pip3 install "uv>=0.4.12"

# Modify the PATH environment variable
ENV PATH="/home/${USER}/.local/bin:${PATH}"
# Create venv somewhere not conflicting with host venv
ENV UV_PROJECT_ENVIRONMENT="/home/${USER}/.venv"

# Copy the uv files
COPY pyproject.toml uv.lock ./

# Switch back to root to modify the permissions
USER root
RUN chown -R ${UID}:${UID} /app
USER ${UID}

# Copy ssh config
RUN mkdir -p ~/.ssh
RUN ssh-keyscan -H git-codecommit.eu-west-1.amazonaws.com >> ~/.ssh/known_hosts 2>/dev/null
RUN printenv SSH_PRIVATE_KEY > ~/.ssh/id_rsa && chmod 600 ~/.ssh/id_rsa
RUN printenv SSH_CONFIG > ~/.ssh/config && chmod 600 ~/.ssh/config

# We cannot install project yet as code will be attached as a volume on deployment.
RUN uv sync --no-dev --no-install-project --no-editable