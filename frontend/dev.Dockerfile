FROM oven/bun:1.1.0-alpine
ARG VITE_APP_BACKEND_HOST
ARG VITE_APP_BACKEND_PORT
ARG VITE_APP_API_KEY
ARG VITE_APP_BACKEND_API_BASE

WORKDIR /app
ARG UID=1000

# Add user if it doesn't exist
RUN if ! getent passwd $UID &>/dev/null; then adduser -u $UID -D -g '' alpine; fi
USER $UID

# Start the application in dev mode (hot-code reloading, error reporting, etc.)
CMD bun install && bun run dev --host