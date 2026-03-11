"""
Router: /repo
Load repositories (Git URL / local folder / ZIP) and manage the library.
"""

from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.core.state import (
    DATA_DIR,
    WORKSPACE_DIR,
    _normalize_language,
    activate_repo_assets,
    ensure_workspace,
    library_entry_key,
    load_functional_library,
    load_repo_library,
    parse_library_entry_key,
    resolve_library_entry_assets,
    reset_workspace,
    resolve_code_json,
    set_mkdocs_port,
    snapshot_repo_assets,
    upsert_library_entry,
)
from app.core.state import IN_DIR, OUT_DIR  # noqa: F401
from app.schemas.repo_doc import LibraryEntryResponse, LibraryResponse, RepoStateResponse

router = APIRouter(prefix="/repo", tags=["Repository"])


def _load_repository(source: str, source_type: str) -> tuple[str, str, Optional[str]]:
    """
    Delegate to the original loader logic, adapting paths to the data directory.
    Returns (repo_path, repo_name, owner).
    """
    from app.src.loader import load_from_zip, load_from_folder, load_repository

    IN_DIR.mkdir(parents=True, exist_ok=True)
    st = source_type.lower().replace(" ", "_").replace("-", "_")

    if st in ("zip", "zip_file"):
        return load_from_zip(source)
    if st in ("local_folder", "folder", "local"):
        return load_from_folder(source)
    # git_url or fallback
    return load_repository(source)


def _run_repo_map(repo_path: str, repo_name: str) -> tuple[dict, Path]:
    """Run repo_map and return (result dict, code_json_path)."""
    from app.src.repo_mapping import repo_map

    output_dir = str(OUT_DIR / repo_name)
    result = repo_map(repo_path, output_dir)
    code_json_path = Path(output_dir) / "code.json"
    return result, code_json_path


def _start_mkdocs(repo_name: str, repo_url: Optional[str] = None, author: Optional[str] = None) -> Optional[int]:
    from app.src.mkdocs_ui import generate_mkdocs_config, serve_mkdocs

    generate_mkdocs_config(
        project_root=WORKSPACE_DIR,
        repo_name=repo_name,
        repo_url=repo_url,
        author=author,
    )
    port, err = serve_mkdocs(WORKSPACE_DIR, port=None, force_restart=True)
    if err:
        print(f"[repo] MkDocs failed: {err}")
        return None
    set_mkdocs_port(port)
    return port


def _graph_data(graph_path: Optional[str]) -> Optional[dict]:
    if not graph_path:
        return None
    p = Path(graph_path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/load", summary="Load a repository from Git URL or local folder")
async def load_repo(
    source: str = Form(...),
    source_type: str = Form(...),
    language: str = Form("EN-US"),
):
    """
    Map a repository and return initial state.
    This only loads+maps — doc generation is a separate step via /docs/generate.
    """
    ensure_workspace()
    reset_workspace()

    try:
        repo_path, repo_name, owner = _load_repository(source, source_type)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    try:
        result, code_json_path = _run_repo_map(repo_path, repo_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Repository mapping failed: {exc}")

    normalized_lang = _normalize_language(language)
    graph_path_str = result.get("graph_file") or str(Path(str(OUT_DIR / repo_name)) / "graphs" / "graph.json")
    graph_path = graph_path_str if Path(graph_path_str).exists() else None

    entry_key, entry = upsert_library_entry(
        repo_name,
        {
            "repo_path": repo_path,
            "owner": owner,
            "output_dir": str(OUT_DIR / repo_name),
            "graph_path": graph_path or "",
            "repo_url": source if "http" in source_type.lower() or source.startswith("http") else None,
            "source": source,
            "source_type": source_type,
            "language": normalized_lang,
            "docs_available": False,
            "functional_docs_available": False,
        },
        language=normalized_lang,
    )

    # Copy code.json to library dir immediately so /docs/generate can find it
    try:
        from app.core.state import _library_repo_dir_for_language
        import shutil as _shutil
        lib_repo_dir = _library_repo_dir_for_language(repo_name, normalized_lang)
        lib_repo_dir.mkdir(parents=True, exist_ok=True)
        if code_json_path.exists():
            _shutil.copy2(code_json_path, lib_repo_dir / "code.json")
        if graph_path and Path(graph_path).exists():
            _shutil.copy2(graph_path, lib_repo_dir / "graph.json")
    except Exception as copy_exc:
        print(f"[repo] Warning: could not copy assets to library: {copy_exc}")

    return RepoStateResponse(
        repo_name=repo_name,
        repo_path=repo_path,
        owner=owner,
        language=normalized_lang,
        output_dir=str(OUT_DIR / repo_name),
        graph_path=graph_path,
        docs_generated=False,
        functional_docs_generated=False,
        docs_skipped=True,
        doc_variant="technical",
        generation_mode="technical_only",
        library_entry_key=entry_key,
        result=result,
    )


@router.post("/upload", summary="Upload a ZIP file to be used as repository source")
async def upload_zip(file: UploadFile = File(...)):
    """
    Accept a ZIP upload, save it to the in/ directory, and return the path
    to be passed to POST /repo/load with source_type=zip.
    """
    IN_DIR.mkdir(parents=True, exist_ok=True)
    dest = IN_DIR / file.filename
    try:
        content = await file.read()
        dest.write_bytes(content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {exc}")
    return {"filename": file.filename, "path": str(dest)}


@router.get("/library", response_model=LibraryResponse, summary="List all saved repositories")
async def list_library(kind: str = "technical"):
    """
    Return all saved technical (kind=technical) or functional (kind=functional) library entries.
    """
    if kind == "functional":
        raw = load_functional_library()
    else:
        raw = load_repo_library()

    entries: list[LibraryEntryResponse] = []
    for entry_key, entry in raw.items():
        if not isinstance(entry, dict):
            continue
        parsed_repo, _ = parse_library_entry_key(entry_key)
        repo_name = (entry.get("repo_name") or parsed_repo or "").strip()
        if not repo_name:
            continue
        resolved = resolve_library_entry_assets(repo_name, entry)
        entries.append(
            LibraryEntryResponse(
                repo_name=repo_name,
                language=_normalize_language(resolved.get("language")),
                entry_key=entry_key,
                updated_at=resolved.get("updated_at"),
                docs_available=bool(resolved.get("docs_available")),
                functional_docs_available=bool(resolved.get("functional_docs_available")),
                repo_url=resolved.get("repo_url"),
                source_type=resolved.get("source_type"),
            )
        )

    # Sort newest first
    entries.sort(key=lambda e: e.updated_at or "", reverse=True)
    return LibraryResponse(entries=entries)


@router.delete("/library/{entry_key:path}", summary="Remove a repository from the library")
async def delete_library_entry(entry_key: str, kind: str = "technical"):
    if kind == "functional":
        from app.core.state import load_functional_library, save_functional_library

        lib = load_functional_library()
        if entry_key not in lib:
            raise HTTPException(status_code=404, detail="Entry not found in functional library.")
        lib.pop(entry_key)
        save_functional_library(lib)
    else:
        from app.core.state import load_repo_library, save_repo_library

        lib = load_repo_library()
        if entry_key not in lib:
            raise HTTPException(status_code=404, detail="Entry not found in library.")
        lib.pop(entry_key)
        save_repo_library(lib)

    return {"deleted": True, "entry_key": entry_key}


@router.post("/activate", summary="Activate a library entry into the workspace")
async def activate_library_entry(
    entry_key: str = Form(...),
    doc_variant: str = Form("technical"),
    start_mkdocs: bool = Form(True),
):
    """
    Copy a saved library entry's docs/assets into the active workspace and
    optionally start/restart the MkDocs server.
    """
    from app.core.state import load_repo_library

    library = load_repo_library()
    entry = library.get(entry_key)
    if not isinstance(entry, dict):
        raise HTTPException(status_code=404, detail="Library entry not found.")

    parsed_repo, _ = parse_library_entry_key(entry_key)
    repo_name = (entry.get("repo_name") or parsed_repo or "").strip()
    resolved = resolve_library_entry_assets(repo_name, entry)
    docs_ok = activate_repo_assets(resolved, doc_variant=doc_variant)
    if not docs_ok:
        reset_workspace()

    port = None
    if start_mkdocs:
        port = _start_mkdocs(
            repo_name,
            repo_url=resolved.get("repo_url"),
            author=resolved.get("owner"),
        )

    graph_path = resolved.get("library_graph_json") or ""
    graph_file = Path(graph_path) if graph_path else Path("")
    code_json = Path(resolved.get("library_code_json") or "")
    if not code_json.exists():
        code_json_resolved = resolve_code_json(repo_name, resolved.get("language"))
        code_json = code_json_resolved or code_json

    return RepoStateResponse(
        repo_name=repo_name,
        repo_path=resolved.get("repo_path"),
        owner=resolved.get("owner"),
        language=_normalize_language(resolved.get("language")),
        output_dir=str(code_json.parent) if code_json.exists() else resolved.get("output_dir"),
        graph_path=str(graph_file) if graph_file.exists() else None,
        docs_generated=bool(docs_ok),
        functional_docs_generated=bool(resolved.get("functional_docs_available")),
        docs_skipped=not docs_ok,
        doc_variant=doc_variant,
        generation_mode=resolved.get("generation_mode") or "technical_only",
        mkdocs_port=port,
        library_entry_key=entry_key,
    )