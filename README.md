# EXAMPLE PROJECT SETUP

This repo containes a bare project setup for a simple GenMS pilot project. It contains a basic project structure, with two containeraized services, a simple web frontend and backend. This project should be used as a starting point for new projects in GenMS.

## Important files to be aware of

This project is a template project, and should be adapted to your specific use case. Changes should be made to the whole project, but specifically to the following files:

### Root folder
These changes should be made to ensure the project is correctly named and configured for your project.
- `example.code-workspace`: Change the name of the workspace file to your project name.
- `README.md`: Change the content of the README file to reflect your project.
- `docker-compose.yml` and `dev.docker-compose.yml`: Change the name of the services from example-backend and example-frontend to your project name, along with all other references to the project name in its args.
- `.env.secrets`, `.env.secrets_defaults`, `.env.defaults`: Add the necessary environment variables.

### Backend folder

- `Dockerfile`and `dev.Dockerfile`: Change the following code snippet to reflect your project name:
```dockerfile
ENV PROJECT_NAME "EXAMPLE"
```
This change allows for llm calls and database monitoring to be correctly configured for your project.

- `app/routers/example.py': Change the file name and following code snippet to reflect your project name in your backend calls:
```python
router = APIRouter(prefix="/example", tags=["Example Project"])
```

### Frontend folder
- `vite.config.mts`: Change the following code snippet to reflect your project name:
```typescript
  server: {
    port: 3000,
    proxy: {
      '/example': { target: 'http://example-backend:8000', changeOrigin: true },
      '/docs': { target: 'http://example-backend:8000', changeOrigin: true },
    },
  },
```
