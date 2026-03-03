# ---- Base Bun ----
FROM oven/bun:1.1.0-alpine
ARG VITE_APP_BACKEND_HOST
ARG VITE_APP_BACKEND_PORT
ARG VITE_APP_API_KEY
ARG VITE_APP_BACKEND_API_BASE

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Change the user if it doesn't exist and set permissions
RUN if ! getent passwd $UID &>/dev/null; then adduser -u $UID -D -g '' alpine; fi

USER $UID

# Install the application dependencies
RUN bun install

# Build the application
RUN bun run build

# Start the application in production mode
CMD bun run preview --host --port ${UI_PORT}

