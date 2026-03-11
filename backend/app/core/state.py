"""
app/core/state.py

Centralised in-process state shared across all request handlers.
Keeps LLM credentials, repository library (JSON-on-disk), chat history,
and the live MkDocs subprocess reference.

NOTE: This module uses simple in-memory + JSON-file persistence — intentionally
keeping the same storage model as the original Streamlit app so no database
migration is needed.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# File-system layout (mirrors the Streamlit app)
# ---------------------------------------------------------------------------

DATA_DIR = Path(os.environ.get("APP_DATA_DIR", "/app/data"))
LIBRARY_DIR = DATA_DIR / "library"
REPO_LIBRARY_FILE = LIBRARY_DIR / "library.json"
REPO_ASSETS_DIR = LIBRARY_DIR / "repos"

FUNCTIONAL_LIBRARY_DIR = DATA_DIR / "library_functional"
FUNCTIONAL_REPO_LIBRARY_FILE = FUNCTIONAL_LIBRARY_DIR / "library.json"
FUNCTIONAL_REPO_ASSETS_DIR = FUNCTIONAL_LIBRARY_DIR / "repos"

CHAT_HISTORY_DIR = DATA_DIR / ".chat_history"
LLM_CONFIG_FILE = DATA_DIR / ".llm_config.json"
WORKSPACE_DIR = DATA_DIR / "workspace"   # active docs/graphs live here
IN_DIR = DATA_DIR / "in"                 # cloned / extracted repos
OUT_DIR = DATA_DIR / "out"               # repo_map outputs (code.json, graphs)

MAX_CHAT_HISTORY = 200

# ---------------------------------------------------------------------------
# In-memory LLM runtime credentials (not persisted across restarts)
# ---------------------------------------------------------------------------

_LLM_RUNTIME_KEYS: dict[str, str] = {}
_BEDROCK_ENV_BACKUP: dict[str, Optional[str]] = {}
_BEDROCK_ENV_ACTIVE: bool = False


def set_runtime_key(provider: str, api_key: Optional[str]) -> None:
    if not provider:
        return
    if api_key:
        _LLM_RUNTIME_KEYS[provider] = api_key
    else:
        _LLM_RUNTIME_KEYS.pop(provider, None)


def get_runtime_key(provider: str) -> Optional[str]:
    return _LLM_RUNTIME_KEYS.get(provider) or None


def set_bedrock_credentials(
    provider: str,
    use_system_key: bool,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> None:
    global _BEDROCK_ENV_BACKUP, _BEDROCK_ENV_ACTIVE

    if provider != "bedrock":
        _restore_bedrock_credentials()
        return

    access = str(access_key or "").strip()
    secret = str(secret_key or "").strip()
    if use_system_key or not access or not secret:
        _restore_bedrock_credentials()
        return

    if not _BEDROCK_ENV_ACTIVE:
        _BEDROCK_ENV_BACKUP = {
            "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        }
    os.environ["AWS_ACCESS_KEY_ID"] = access
    os.environ["AWS_SECRET_ACCESS_KEY"] = secret
    _BEDROCK_ENV_ACTIVE = True


def _restore_bedrock_credentials() -> None:
    global _BEDROCK_ENV_BACKUP, _BEDROCK_ENV_ACTIVE
    if not _BEDROCK_ENV_ACTIVE:
        return
    for key in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"):
        prev = _BEDROCK_ENV_BACKUP.get(key)
        if prev is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = prev
    _BEDROCK_ENV_BACKUP = {}
    _BEDROCK_ENV_ACTIVE = False


# ---------------------------------------------------------------------------
# LLM Config persistence
# ---------------------------------------------------------------------------

def load_llm_config() -> dict:
    try:
        if LLM_CONFIG_FILE.exists():
            data = json.loads(LLM_CONFIG_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}


def save_llm_config(
    provider: str,
    model: str,
    use_system_key: bool,
    api_key: Optional[str] = None,
    bedrock_access_key: Optional[str] = None,
    bedrock_secret_key: Optional[str] = None,
) -> None:
    try:
        LLM_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        existing = load_llm_config()
        payload = {
            "provider": provider,
            "model": model,
            "use_system_key": bool(use_system_key),
            "api_key": "" if use_system_key else (api_key or ""),
            "bedrock_access_key": str(existing.get("bedrock_access_key") or ""),
            "bedrock_secret_key": str(existing.get("bedrock_secret_key") or ""),
        }
        if provider == "bedrock":
            payload["bedrock_access_key"] = "" if use_system_key else str(bedrock_access_key or "")
            payload["bedrock_secret_key"] = "" if use_system_key else str(bedrock_secret_key or "")
        LLM_CONFIG_FILE.write_text(json.dumps(payload), encoding="utf-8")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Library helpers
# ---------------------------------------------------------------------------

def _repo_slug(repo_name: str) -> str:
    import re
    value = (repo_name or "").strip()
    if not value:
        return "repo"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)


def _normalize_language(language: Optional[str]) -> str:
    value = (language or "").strip().upper()
    if value.startswith("PT"):
        return "PT-BR"
    if value.startswith("EN"):
        return "EN-US"
    if value.startswith("ES"):
        return "ES-ES"
    if value.startswith("FR"):
        return "FR-FR"
    if value.startswith("DE"):
        return "DE-DE"
    return "EN-US"


def library_entry_key(repo_name: str, language: Optional[str]) -> str:
    lang = _normalize_language(language)
    return f"{repo_name}::{lang}"


def parse_library_entry_key(entry_key: str) -> tuple[str, Optional[str]]:
    if "::" in (entry_key or ""):
        repo, lang = entry_key.split("::", 1)
        return repo, _normalize_language(lang)
    return entry_key, None


def _library_repo_dir_for_language(repo_name: str, language: Optional[str]) -> Path:
    lang = _normalize_language(language)
    return REPO_ASSETS_DIR / f"{_repo_slug(repo_name)}__{_repo_slug(lang)}"


def _functional_library_repo_dir_for_language(repo_name: str, language: Optional[str]) -> Path:
    lang = _normalize_language(language)
    return FUNCTIONAL_REPO_ASSETS_DIR / f"{_repo_slug(repo_name)}__{_repo_slug(lang)}"


def load_repo_library() -> dict:
    try:
        if REPO_LIBRARY_FILE.exists():
            data = json.loads(REPO_LIBRARY_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}


def save_repo_library(data: dict) -> None:
    try:
        REPO_LIBRARY_FILE.parent.mkdir(parents=True, exist_ok=True)
        REPO_LIBRARY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def load_functional_library() -> dict:
    try:
        if FUNCTIONAL_REPO_LIBRARY_FILE.exists():
            data = json.loads(FUNCTIONAL_REPO_LIBRARY_FILE.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception:
        pass
    return {}


def save_functional_library(data: dict) -> None:
    try:
        FUNCTIONAL_REPO_LIBRARY_FILE.parent.mkdir(parents=True, exist_ok=True)
        FUNCTIONAL_REPO_LIBRARY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def upsert_library_entry(repo_name: str, updates: dict, language: Optional[str] = None) -> tuple[str, dict]:
    repo_name = (repo_name or "").strip()
    if not repo_name:
        return "", {}
    normalized_lang = _normalize_language(language or updates.get("language"))
    entry_key = updates.get("entry_key") or library_entry_key(repo_name, normalized_lang)
    library = load_repo_library()
    current = library.get(entry_key, {})
    merged = dict(current)
    merged.update(updates)
    merged["repo_name"] = repo_name
    merged["language"] = normalized_lang
    merged["entry_key"] = entry_key
    merged["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    library[entry_key] = merged
    save_repo_library(library)
    return entry_key, merged


def upsert_functional_library_entry(repo_name: str, updates: dict, language: Optional[str] = None) -> tuple[str, dict]:
    repo_name = (repo_name or "").strip()
    if not repo_name:
        return "", {}
    normalized_lang = _normalize_language(language or updates.get("language"))
    entry_key = updates.get("entry_key") or library_entry_key(repo_name, normalized_lang)
    library = load_functional_library()
    current = library.get(entry_key, {})
    merged = dict(current)
    merged.update(updates)
    merged["repo_name"] = repo_name
    merged["language"] = normalized_lang
    merged["entry_key"] = entry_key
    merged["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    library[entry_key] = merged
    save_functional_library(library)
    return entry_key, merged


def resolve_library_entry_assets(repo_name: str, entry: dict) -> dict:
    """Fill in missing asset paths based on expected on-disk layout."""
    resolved = dict(entry or {})
    lang = resolved.get("language")
    repo_dir = _library_repo_dir_for_language(repo_name, lang)
    defaults = {
        "library_repo_dir": str(repo_dir),
        "library_docs_dir": str(repo_dir / "docs"),
        "library_code_json": str(repo_dir / "code.json"),
        "library_documentation_md": str(repo_dir / "documentation.md"),
        "library_functional_docs_dir": str(repo_dir / "docs_functional"),
        "library_functional_documentation_md": str(repo_dir / "functional_documentation.md"),
        "library_graph_json": str(repo_dir / "graph.json"),
    }
    for key, fallback in defaults.items():
        current = str(resolved.get(key) or "").strip()
        if current and Path(current).exists():
            resolved[key] = current
        elif Path(fallback).exists():
            resolved[key] = fallback
        else:
            resolved[key] = fallback

    docs_dir = Path(str(resolved.get("library_docs_dir") or ""))
    resolved["docs_available"] = bool(docs_dir.exists() and any(docs_dir.glob("*.md")))
    func_dir = Path(str(resolved.get("library_functional_docs_dir") or ""))
    resolved["functional_docs_available"] = bool(func_dir.exists() and any(func_dir.glob("*.md")))
    return resolved


def snapshot_repo_assets(
    repo_name: str,
    code_json_path: Path,
    language: str,
    graph_path: Optional[str] = None,
    include_functional: bool = False,
) -> dict:
    """Copy generated assets from workspace into library storage."""
    repo_dir = _library_repo_dir_for_language(repo_name, language)
    docs_src = WORKSPACE_DIR / "docs"
    md_src = WORKSPACE_DIR / "documentation.md"
    functional_docs_src = WORKSPACE_DIR / "docs_functional"
    functional_md_src = WORKSPACE_DIR / "functional_documentation.md"

    payload: dict[str, Any] = {
        "library_repo_dir": str(repo_dir),
        "library_docs_dir": str(repo_dir / "docs"),
        "library_code_json": str(repo_dir / "code.json"),
        "library_documentation_md": str(repo_dir / "documentation.md"),
        "library_functional_docs_dir": str(repo_dir / "docs_functional"),
        "library_functional_documentation_md": str(repo_dir / "functional_documentation.md"),
        "library_graph_json": "",
        "docs_available": False,
        "functional_docs_available": False,
    }

    try:
        repo_dir.mkdir(parents=True, exist_ok=True)
        if code_json_path.exists():
            shutil.copy2(code_json_path, repo_dir / "code.json")

        docs_dst = repo_dir / "docs"
        if docs_dst.exists():
            shutil.rmtree(docs_dst)
        if docs_src.exists():
            shutil.copytree(docs_src, docs_dst)
            payload["docs_available"] = any(docs_dst.glob("*.md"))

        md_dst = repo_dir / "documentation.md"
        if md_src.exists():
            shutil.copy2(md_src, md_dst)

        if include_functional:
            fdocs_dst = repo_dir / "docs_functional"
            if fdocs_dst.exists():
                shutil.rmtree(fdocs_dst)
            if functional_docs_src.exists():
                shutil.copytree(functional_docs_src, fdocs_dst)
                payload["functional_docs_available"] = any(fdocs_dst.glob("*.md"))
            fmd_dst = repo_dir / "functional_documentation.md"
            if functional_md_src.exists():
                shutil.copy2(functional_md_src, fmd_dst)
                payload["functional_docs_available"] = bool(payload["functional_docs_available"] or fmd_dst.exists())

        if graph_path and Path(graph_path).exists():
            graph_dst = repo_dir / "graph.json"
            shutil.copy2(graph_path, graph_dst)
            payload["library_graph_json"] = str(graph_dst)
    except Exception as exc:
        print(f"[state] snapshot_repo_assets error: {exc}")

    return payload


def snapshot_functional_assets(
    repo_name: str,
    language: str,
    graph_path: Optional[str] = None,
    code_json_path: Optional[Path] = None,
) -> dict:
    repo_dir = _functional_library_repo_dir_for_language(repo_name, language)
    docs_src = WORKSPACE_DIR / "docs_functional"
    md_src = WORKSPACE_DIR / "functional_documentation.md"

    payload: dict[str, Any] = {
        "library_repo_dir": str(repo_dir),
        "library_docs_dir": str(repo_dir / "docs_functional"),
        "library_functional_docs_dir": str(repo_dir / "docs_functional"),
        "library_functional_documentation_md": str(repo_dir / "functional_documentation.md"),
        "library_graph_json": "",
        "docs_available": False,
        "functional_docs_available": False,
    }

    try:
        repo_dir.mkdir(parents=True, exist_ok=True)
        fdocs_dst = repo_dir / "docs_functional"
        if fdocs_dst.exists():
            shutil.rmtree(fdocs_dst)
        if docs_src.exists():
            shutil.copytree(docs_src, fdocs_dst)
            payload["functional_docs_available"] = any(fdocs_dst.glob("*.md"))

        fmd_dst = repo_dir / "functional_documentation.md"
        if md_src.exists():
            shutil.copy2(md_src, fmd_dst)
            payload["functional_docs_available"] = bool(payload["functional_docs_available"] or fmd_dst.exists())
        payload["docs_available"] = bool(payload["functional_docs_available"])

        if code_json_path and code_json_path.exists():
            shutil.copy2(code_json_path, repo_dir / "code.json")

        if graph_path and Path(graph_path).exists():
            graph_dst = repo_dir / "graph.json"
            shutil.copy2(graph_path, graph_dst)
            payload["library_graph_json"] = str(graph_dst)
    except Exception as exc:
        print(f"[state] snapshot_functional_assets error: {exc}")

    return payload


def activate_repo_assets(entry: dict, doc_variant: str = "technical") -> bool:
    """Copy library assets into the active workspace."""
    variant = str(doc_variant or "technical").strip().lower()

    def _p(value: Any) -> Optional[Path]:
        raw = str(value or "").strip()
        if not raw or raw in {".", "./", ".\\"}:
            return None
        try:
            return Path(raw)
        except Exception:
            return None

    if variant == "functional":
        docs_src = _p(entry.get("library_functional_docs_dir"))
        md_src = _p(entry.get("library_functional_documentation_md"))
    else:
        docs_src = _p(entry.get("library_docs_dir"))
        md_src = _p(entry.get("library_documentation_md"))

    docs_dst = WORKSPACE_DIR / "docs"
    md_dst = WORKSPACE_DIR / "documentation.md"
    restored = False

    try:
        if docs_dst.exists():
            shutil.rmtree(docs_dst)
        if docs_src and docs_src.exists():
            shutil.copytree(docs_src, docs_dst)
            restored = True
        if md_dst.exists():
            md_dst.unlink()
        if md_src and md_src.exists():
            shutil.copy2(md_src, md_dst)
    except Exception as exc:
        print(f"[state] activate_repo_assets error: {exc}")
        return False

    # Optional functional sidecar sync
    func_docs_src = _p(entry.get("library_functional_docs_dir"))
    func_md_src = _p(entry.get("library_functional_documentation_md"))
    func_docs_dst = WORKSPACE_DIR / "docs_functional"
    func_md_dst = WORKSPACE_DIR / "functional_documentation.md"
    try:
        if func_docs_src and func_docs_src.exists():
            if func_docs_dst.exists():
                shutil.rmtree(func_docs_dst)
            shutil.copytree(func_docs_src, func_docs_dst)
        if func_md_src and func_md_src.exists():
            if func_md_dst.exists():
                func_md_dst.unlink()
            shutil.copy2(func_md_src, func_md_dst)
    except Exception:
        pass

    return restored


# ---------------------------------------------------------------------------
# Chat history persistence
# ---------------------------------------------------------------------------

def _chat_path(repo_name: str, session_id: Optional[str] = None) -> Path:
    if session_id:
        return CHAT_HISTORY_DIR / f"{repo_name}__{session_id}.json"
    return CHAT_HISTORY_DIR / f"{repo_name}.json"


def load_chat_history(repo_name: str, session_id: Optional[str] = None) -> list[dict]:
    try:
        path = _chat_path(repo_name, session_id)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def save_chat_history(repo_name: str, history: list[dict], session_id: Optional[str] = None) -> None:
    try:
        CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        trimmed = history[-MAX_CHAT_HISTORY:]
        path = _chat_path(repo_name, session_id)
        path.write_text(json.dumps(trimmed, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def clear_chat_history(repo_name: str, session_id: Optional[str] = None) -> None:
    try:
        path = _chat_path(repo_name, session_id)
        if path.exists():
            path.unlink()
    except Exception:
        pass


def list_chat_sessions(repo_name: str) -> list[dict]:
    """Return [{session_id, title, updated_at}] for all sessions of this repo, newest first."""
    try:
        CHAT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        sessions = []
        for f in CHAT_HISTORY_DIR.glob(f"{repo_name}*.json"):
            stem = f.stem  # e.g. "myrepo" or "myrepo__<uuid>"
            if stem == repo_name:
                sid = "__default__"
            elif stem.startswith(repo_name + "__"):
                sid = stem[len(repo_name) + 2:]
            else:
                continue
            try:
                history = json.loads(f.read_text(encoding="utf-8"))
                first_user = next((m["content"] for m in history if m.get("role") == "user"), "")
                sessions.append({
                    "session_id": sid,
                    "title": first_user[:60] if first_user else "New chat",
                    "updated_at": f.stat().st_mtime,
                })
            except Exception:
                continue
        sessions.sort(key=lambda s: s["updated_at"], reverse=True)
        return sessions
    except Exception:
        return []


# ---------------------------------------------------------------------------
# MkDocs port tracking
# ---------------------------------------------------------------------------

_MKDOCS_PORT: Optional[int] = None


def get_mkdocs_port() -> Optional[int]:
    return _MKDOCS_PORT


def set_mkdocs_port(port: Optional[int]) -> None:
    global _MKDOCS_PORT
    _MKDOCS_PORT = port


def is_port_open(port: Optional[int]) -> bool:
    try:
        if not port:
            return False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.25)
            return s.connect_ex(("127.0.0.1", int(port))) == 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Workspace helpers
# ---------------------------------------------------------------------------

def reset_workspace() -> None:
    """Clear active docs from workspace (does NOT touch library)."""
    for name in ("docs", "documentation.md", "docs_functional", "functional_documentation.md"):
        target = WORKSPACE_DIR / name
        try:
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
        except Exception:
            pass


def workspace_path(relative: str) -> Path:
    return WORKSPACE_DIR / relative


def ensure_workspace() -> None:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


def resolve_code_json(repo_name: str, preferred_language: Optional[str] = None) -> Optional[Path]:
    """Find the best code.json for a repo in the library."""
    library = load_repo_library()
    preferred_lang = _normalize_language(preferred_language)
    candidates: list[tuple[int, str, Path]] = []
    for entry_key, entry in library.items():
        if not isinstance(entry, dict):
            continue
        parsed_repo, _ = parse_library_entry_key(entry_key)
        entry_repo = entry.get("repo_name") or parsed_repo
        if entry_repo != repo_name:
            continue
        resolved = resolve_library_entry_assets(entry_repo, entry)
        path_str = resolved.get("library_code_json", "")
        if not path_str or not Path(path_str).exists():
            continue
        entry_lang = _normalize_language(resolved.get("language"))
        score = 1 if entry_lang == preferred_lang else 0
        updated = str(resolved.get("updated_at") or "")
        candidates.append((score, updated, Path(path_str)))
    if candidates:
        candidates.sort(key=lambda r: (r[0], r[1]), reverse=True)
        return candidates[0][2]
    return None
