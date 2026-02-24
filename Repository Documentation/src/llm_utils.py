import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from langchain.chat_models import init_chat_model

DEFAULT_GEMINI_API_KEY = "AIzaSyD51liDLCePQcVM7PhF00LFwq92C-ZiFcg"
DEFAULT_BEDROCK_TIMEOUT_SECONDS = 180.0
DEFAULT_BEDROCK_REGION = "us-east-1"
BEDROCK_HAIKU_45_MODEL_ID = "anthropic.claude-haiku-4-5-20251001-v1:0"
BEDROCK_HAIKU_45_PROFILE_ENV = "BEDROCK_HAIKU_45_INFERENCE_PROFILE_ARN"
BEDROCK_ALLOW_CROSS_REGION_ENV = "BEDROCK_ALLOW_CROSS_REGION_PROFILE"

PROVIDER_LABELS = {
    "gemini": "Gemini",
    "openai": "GPT (OpenAI)",
    "bedrock": "Amazon Bedrock (LiteLLM)",
}

PROVIDER_ENV_VARS = {
    "gemini": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
}
BEDROCK_INFERENCE_PROFILE_FALLBACKS = {
    # Foundation model IDs that require inference profile in Bedrock.
    BEDROCK_HAIKU_45_MODEL_ID: "us.anthropic.claude-haiku-4-5-20251001-v1:0",
}


def _read_ini_sections(path: Path) -> list[str]:
    parser = ConfigParser()
    try:
        parser.read(path, encoding="utf-8")
    except Exception:
        return []
    return [str(section).strip() for section in parser.sections() if str(section).strip()]


def _normalize_config_profile(section_name: str) -> str:
    raw = str(section_name or "").strip()
    if not raw:
        return ""
    if raw.lower().startswith("profile "):
        return raw[8:].strip()
    return raw


def _resolve_local_aws_profile(credentials_path: Path, config_path: Path) -> Optional[str]:
    if os.getenv("AWS_PROFILE"):
        return os.getenv("AWS_PROFILE")
    profiles: list[str] = []
    if credentials_path.exists():
        profiles.extend(_read_ini_sections(credentials_path))
    if config_path.exists():
        profiles.extend(
            _normalize_config_profile(section)
            for section in _read_ini_sections(config_path)
        )
    unique = []
    seen = set()
    for name in profiles:
        key = str(name or "").strip()
        if not key:
            continue
        lowered = key.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(key)
    if not unique:
        return None
    for preferred in ("default", "bedrock-dev"):
        for name in unique:
            if name.lower() == preferred:
                return name
    if len(unique) == 1:
        return unique[0]
    return None


def _resolve_local_aws_region(config_path: Path, profile: Optional[str]) -> Optional[str]:
    if os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"):
        return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if not config_path.exists():
        return None
    parser = ConfigParser()
    try:
        parser.read(config_path, encoding="utf-8")
    except Exception:
        return None
    candidates = []
    if profile:
        candidates.append(f"profile {profile}")
        candidates.append(profile)
    candidates.append("default")
    for section_name in candidates:
        if parser.has_section(section_name):
            region = str(parser.get(section_name, "region", fallback="") or "").strip()
            if region:
                return region
    return None


def _configure_local_bedrock_aws_env() -> None:
    # Allow project-local .aws credentials/config without requiring shell exports.
    workspace_root = Path.cwd()
    local_aws_dir = workspace_root / ".aws"
    credentials_path = local_aws_dir / "credentials"
    config_path = local_aws_dir / "config"
    if credentials_path.exists():
        os.environ.setdefault("AWS_SHARED_CREDENTIALS_FILE", str(credentials_path))
    if config_path.exists():
        os.environ.setdefault("AWS_CONFIG_FILE", str(config_path))
    profile = _resolve_local_aws_profile(credentials_path, config_path)
    if profile:
        os.environ.setdefault("AWS_PROFILE", profile)
    # Bedrock invocations for this app must default to us-east-1, unless explicitly overridden.
    forced_region = str(os.getenv("BEDROCK_REGION") or "").strip()
    region = forced_region or DEFAULT_BEDROCK_REGION
    os.environ["AWS_REGION"] = region
    os.environ["AWS_DEFAULT_REGION"] = region
    os.environ["AWS_REGION_NAME"] = region
    os.environ["AWS_BEDROCK_RUNTIME_ENDPOINT"] = f"https://bedrock-runtime.{region}.amazonaws.com"


def normalize_provider(provider: str) -> str:
    value = (provider or "").strip().lower()
    if value in ("gemini", "google", "google_genai"):
        return "gemini"
    if value in ("openai", "gpt"):
        return "openai"
    if value in ("bedrock", "aws_bedrock", "amazon_bedrock"):
        return "bedrock"
    raise ValueError(f"Unsupported provider: {provider}")


def _normalize_bedrock_model_name(model_name: str) -> str:
    value = (model_name or "").strip()
    if not value:
        return ""
    if value.startswith("arn:aws:bedrock:"):
        marker = "foundation-model/"
        idx = value.find(marker)
        if idx >= 0:
            value = value[idx + len(marker):].strip()
        else:
            # Keep inference-profile/application-inference-profile ARNs as provided.
            return value
    if value.startswith("bedrock/"):
        value = value.split("/", 1)[1].strip()
    if value == BEDROCK_HAIKU_45_MODEL_ID:
        explicit_profile = str(os.getenv(BEDROCK_HAIKU_45_PROFILE_ENV) or "").strip()
        if explicit_profile:
            return explicit_profile
        fallback_profile = BEDROCK_INFERENCE_PROFILE_FALLBACKS.get(value, value)
        allow_cross_region = str(os.getenv(BEDROCK_ALLOW_CROSS_REGION_ENV) or "").strip().lower() in {
            "1", "true", "yes", "on"
        }
        if fallback_profile != value and not allow_cross_region:
            raise ValueError(
                "Claude Haiku 4.5 on Bedrock requires an inference profile. "
                "The default fallback profile is cross-region and may invoke us-east-2. "
                f"Set {BEDROCK_HAIKU_45_PROFILE_ENV} to a us-east-1 inference profile ARN/ID, "
                f"or set {BEDROCK_ALLOW_CROSS_REGION_ENV}=1 to allow cross-region routing."
            )
    return BEDROCK_INFERENCE_PROFILE_FALLBACKS.get(value, value)


def resolve_api_key(
    provider: str,
    api_key: Optional[str] = None,
    use_system_key: bool = True,
) -> Optional[str]:
    provider = normalize_provider(provider)
    if provider == "bedrock":
        # Bedrock uses AWS credentials from environment/profile/role.
        return None
    if api_key and api_key.strip():
        return api_key.strip()
    if use_system_key:
        if provider == "gemini":
            return DEFAULT_GEMINI_API_KEY or os.getenv(PROVIDER_ENV_VARS[provider])
        return os.getenv(PROVIDER_ENV_VARS[provider])
    return None


def configure_api_key(
    provider: str,
    api_key: Optional[str] = None,
    use_system_key: bool = True,
) -> Optional[str]:
    provider = normalize_provider(provider)
    if provider == "bedrock":
        return None
    key = resolve_api_key(provider, api_key=api_key, use_system_key=use_system_key)
    if key:
        os.environ[PROVIDER_ENV_VARS[provider]] = key
    return key


def init_llm(
    provider: str,
    model_name: str,
    api_key: Optional[str] = None,
    use_system_key: bool = True,
    temperature: float = 0.0,
):
    provider = normalize_provider(provider)
    if provider == "bedrock":
        _configure_local_bedrock_aws_env()
        model_id = _normalize_bedrock_model_name(model_name)
        if not model_id:
            raise ValueError("Model ID do Bedrock não definido.")
        try:
            from langchain_litellm import ChatLiteLLM
        except Exception as exc:
            raise ValueError(
                "Dependência ausente para Bedrock. Instale 'langchain-litellm' e 'litellm'."
            ) from exc
        timeout_value = DEFAULT_BEDROCK_TIMEOUT_SECONDS
        try:
            timeout_value = float(
                os.getenv("BEDROCK_REQUEST_TIMEOUT_SECONDS", str(DEFAULT_BEDROCK_TIMEOUT_SECONDS))
            )
        except Exception:
            timeout_value = DEFAULT_BEDROCK_TIMEOUT_SECONDS
        bedrock_region = str(
            os.getenv("BEDROCK_REGION")
            or os.getenv("AWS_REGION_NAME")
            or os.getenv("AWS_REGION")
            or DEFAULT_BEDROCK_REGION
        ).strip() or DEFAULT_BEDROCK_REGION
        bedrock_runtime_endpoint = (
            str(os.getenv("AWS_BEDROCK_RUNTIME_ENDPOINT") or "").strip()
            or f"https://bedrock-runtime.{bedrock_region}.amazonaws.com"
        )
        bedrock_model_kwargs = {
            "aws_region_name": bedrock_region,
            "aws_bedrock_runtime_endpoint": bedrock_runtime_endpoint,
        }
        print(
            "[llm_utils] bedrock init "
            f"model_id={model_id} region={bedrock_region} "
            f"endpoint={bedrock_runtime_endpoint} profile={os.getenv('AWS_PROFILE') or '-'}"
        )
        try:
            return ChatLiteLLM(
                model=f"bedrock/{model_id}",
                custom_llm_provider="bedrock",
                model_kwargs=bedrock_model_kwargs,
                temperature=temperature,
                timeout=timeout_value,
            )
        except TypeError:
            # Compatibility with wrappers that do not expose timeout.
            return ChatLiteLLM(
                model=f"bedrock/{model_id}",
                custom_llm_provider="bedrock",
                model_kwargs=bedrock_model_kwargs,
                temperature=temperature,
            )

    key = configure_api_key(provider, api_key=api_key, use_system_key=use_system_key)
    if not key:
        env_var = PROVIDER_ENV_VARS[provider]
        label = PROVIDER_LABELS.get(provider, provider)
        raise ValueError(
            f"API key não definida para {label}. "
            f"Informe a chave na interface ou configure {env_var}."
        )
    model_provider = "google_genai" if provider == "gemini" else "openai"
    return init_chat_model(
        model_name,
        model_provider=model_provider,
        temperature=temperature,
    )
