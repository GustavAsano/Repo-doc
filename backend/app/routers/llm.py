"""
Router: /llm
Manage LLM provider settings (save / retrieve).
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.state import (
    load_llm_config,
    save_llm_config,
    set_runtime_key,
    set_bedrock_credentials,
)
from app.schemas.repo_doc import LLMSettingsRequest, LLMSettingsResponse

router = APIRouter(prefix="/llm", tags=["LLM Settings"])


@router.post("/settings", response_model=LLMSettingsResponse, summary="Save LLM provider settings")
async def save_settings(body: LLMSettingsRequest):
    """
    Persist provider / model / key configuration.
    Also applies runtime credentials so subsequent generation calls work immediately.
    """
    provider = (body.provider or "").strip().lower()
    model = (body.model or "").strip()

    # Validate bedrock manual-mode completeness
    if provider == "bedrock" and not body.use_system_key:
        access = str(body.bedrock_access_key or "").strip()
        secret = str(body.bedrock_secret_key or "").strip()
        if not access or not secret:
            return JSONResponse(
                status_code=400,
                content={"error": "Bedrock manual mode requires both AWS access key ID and secret access key."},
            )

    # Persist to disk
    save_llm_config(
        provider=provider,
        model=model,
        use_system_key=body.use_system_key,
        api_key=body.api_key,
        bedrock_access_key=body.bedrock_access_key,
        bedrock_secret_key=body.bedrock_secret_key,
    )

    # Apply runtime credentials
    if provider == "bedrock":
        set_runtime_key(provider, None)
        set_bedrock_credentials(
            provider=provider,
            use_system_key=body.use_system_key,
            access_key=body.bedrock_access_key,
            secret_key=body.bedrock_secret_key,
        )
    else:
        api_key = None if body.use_system_key else (body.api_key or None)
        set_runtime_key(provider, api_key)

    return LLMSettingsResponse(
        provider=provider,
        model=model,
        use_system_key=body.use_system_key,
        saved=True,
    )


@router.get("/settings", response_model=LLMSettingsResponse, summary="Get current LLM settings")
async def get_settings():
    """Return persisted LLM settings (never exposes secret keys)."""
    config = load_llm_config()
    return LLMSettingsResponse(
        provider=config.get("provider") or "gemini",
        model=config.get("model") or "gemini-2.5-flash",
        use_system_key=bool(config.get("use_system_key", True)),
        saved=True,
    )
