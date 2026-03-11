# Code structuring guide

This backend is structured in the following way:

- app/: Application code
- app/core/: Core code, meaning tools, library functions, helpers, etc.
- app/routers/: Router code, meaning API endpoints and their handlers.
- app/schemas/: Schema code, meaning data models, used to validate incoming requests and outgoing responses.
- data/: Data files
- tests/: Unit tests and integration tests