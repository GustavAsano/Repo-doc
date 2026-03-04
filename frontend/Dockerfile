# ---- Build stage ----
FROM oven/bun:1.1.0-alpine AS builder

ARG VITE_APP_BACKEND_HOST
ARG VITE_APP_BACKEND_PORT
ARG VITE_APP_API_KEY
ARG VITE_APP_BACKEND_API_BASE

ENV VITE_APP_BACKEND_HOST=$VITE_APP_BACKEND_HOST
ENV VITE_APP_BACKEND_PORT=$VITE_APP_BACKEND_PORT
ENV VITE_APP_API_KEY=$VITE_APP_API_KEY
ENV VITE_APP_BACKEND_API_BASE=$VITE_APP_BACKEND_API_BASE

WORKDIR /app
COPY . .
RUN bun install --frozen-lockfile
RUN bun run build

# ---- Serve stage ----
FROM nginx:alpine

COPY --from=builder /app/dist /app/dist
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
