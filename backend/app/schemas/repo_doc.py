from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# LLM Settings
# ---------------------------------------------------------------------------

class LLMSettingsRequest(BaseModel):
    provider: str = Field(..., description="LLM provider: gemini | openai | bedrock")
    model: str = Field(..., description="Model name / ID")
    use_system_key: bool = Field(True, description="Use server-side env key")
    api_key: Optional[str] = Field(None, description="User-provided API key (non-bedrock)")
    bedrock_access_key: Optional[str] = Field(None, description="AWS Access Key ID (bedrock manual)")
    bedrock_secret_key: Optional[str] = Field(None, description="AWS Secret Access Key (bedrock manual)")


class LLMSettingsResponse(BaseModel):
    provider: str
    model: str
    use_system_key: bool
    saved: bool = True


# ---------------------------------------------------------------------------
# Repository loading
# ---------------------------------------------------------------------------

class LoadRepoRequest(BaseModel):
    source: str = Field(..., description="Git URL, local path, or uploaded ZIP filename")
    source_type: str = Field(..., description="git_url | local_folder | zip")


class LibraryEntryResponse(BaseModel):
    repo_name: str
    language: str
    entry_key: str
    updated_at: Optional[str] = None
    docs_available: bool = False
    functional_docs_available: bool = False
    repo_url: Optional[str] = None
    source_type: Optional[str] = None


class LibraryResponse(BaseModel):
    entries: list[LibraryEntryResponse]


# ---------------------------------------------------------------------------
# Documentation generation
# ---------------------------------------------------------------------------

class SectionDefinition(BaseModel):
    title: str
    description: str


class GenerateDocRequest(BaseModel):
    repo_name: str
    language: str = "EN-US"
    generation_mode: str = Field(
        "technical_only",
        description="technical_only | technical_and_functional | functional_only",
    )
    documentation_sections: Optional[dict[str, SectionDefinition]] = None
    functional_sections: Optional[dict[str, SectionDefinition]] = None
    # LLM settings inline (validated against server session)
    provider: str = "gemini"
    model: str = "gemini-2.5-flash"
    use_system_key: bool = True
    api_key: Optional[str] = None
    bedrock_access_key: Optional[str] = None
    bedrock_secret_key: Optional[str] = None


class GenerateFromLibraryRequest(BaseModel):
    entry_key: str
    language: str = "EN-US"
    generation_mode: str = "technical_only"
    translate_on_load: bool = False
    provider: str = "gemini"
    model: str = "gemini-2.5-flash"
    use_system_key: bool = True
    api_key: Optional[str] = None
    bedrock_access_key: Optional[str] = None
    bedrock_secret_key: Optional[str] = None
    functional_sections: Optional[dict[str, SectionDefinition]] = None


# ---------------------------------------------------------------------------
# Repo state (returned to frontend after load / generation)
# ---------------------------------------------------------------------------

class RepoStateResponse(BaseModel):
    repo_name: str
    repo_path: Optional[str] = None
    owner: Optional[str] = None
    language: str
    output_dir: Optional[str] = None
    graph_path: Optional[str] = None
    docs_generated: bool = False
    functional_docs_generated: bool = False
    docs_skipped: bool = False
    doc_variant: str = "technical"
    generation_mode: str = "technical_only"
    mkdocs_port: Optional[int] = None
    library_entry_key: Optional[str] = None
    result: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    role: str = Field(..., description="user | assistant")
    content: str


class ChatRequest(BaseModel):
    repo_name: str
    question: str
    session_id: Optional[str] = None
    language: str = "EN-US"
    provider: str = "gemini"
    model: str = "gemini-2.5-flash"
    use_system_key: bool = True
    api_key: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    history: list[ChatMessage]


class ChatHistoryResponse(BaseModel):
    repo_name: str
    history: list[ChatMessage]


class ChatSessionInfo(BaseModel):
    session_id: str
    title: str
    updated_at: float


class ChatSessionsResponse(BaseModel):
    repo_name: str
    sessions: list[ChatSessionInfo]


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

class ExportResponse(BaseModel):
    repo_name: str
    format: str
    filename: str
    # base64-encoded file content
    data: str
    language: str


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

class GraphResponse(BaseModel):
    repo_name: str
    graph: Optional[dict[str, Any]] = None
    available: bool = False


# ---------------------------------------------------------------------------
# MkDocs / Docs server
# ---------------------------------------------------------------------------

class DocsServerResponse(BaseModel):
    port: int
    docs_url: str
    entry_html: str


# ---------------------------------------------------------------------------
# SSE progress event (for streaming)
# ---------------------------------------------------------------------------

class ProgressEvent(BaseModel):
    event: str  # plan | call_start | call_end | done | error
    phase: Optional[str] = None
    current_call: int = 0
    total_calls: int = 0
    message: Optional[str] = None
    is_multi_pass: bool = False
    cost_available: bool = False
    total_cost_usd: Optional[float] = None
    call_cost_usd: Optional[float] = None
