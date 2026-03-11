#!/bin/sh

# Run server
if [ "$BACKEND_DEBUG" = "true" ]; then
    uv sync
    uv run uvicorn app.main:app --host "0.0.0.0" --port ${BACKEND_PORT:-8000} --reload --log-level debug
else
    uv run gunicorn app.main:app --bind "0.0.0.0:${BACKEND_PORT:-8000}" --workers ${BACKEND_NUM_WORKERS:-1} --worker-class uvicorn.workers.UvicornWorker --timeout 600
fi