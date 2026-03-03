import os

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.llm import router as llm_router
from app.routers.repo import router as repo_router
from app.routers.docs import router as docs_router
from app.routers.export import router as export_router
from app.routers.chat import router as chat_router
from app.routers.graph import router as graph_router
from app.core.state import ensure_workspace

ensure_workspace()

app = FastAPI(
    title="Repository Documentation API",
    summary="AI-powered repository documentation generator",
    version="1.0.0",
    root_path=os.environ.get("BACKEND_ROOT_URL", ""),
    redoc_url="/docs",
    docs_url="/docs/swagger",
    openapi_url="/docs/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JSONEncodedError(Exception):
    def __init__(self, status_code: int, content: str):
        self.status_code = status_code
        self.content = content

    def as_response(self):
        return JSONResponse(status_code=self.status_code, content={"error": self.content})

    @classmethod
    def from_exception(cls, exc: Exception) -> "JSONEncodedError":
        if isinstance(exc, cls):
            return exc
        return cls(status_code=500, content=str(exc))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONEncodedError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=str(exc)).as_response()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONEncodedError.from_exception(exc).as_response()


app.include_router(llm_router)
app.include_router(repo_router)
app.include_router(docs_router)
app.include_router(export_router)
app.include_router(chat_router)
app.include_router(graph_router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
