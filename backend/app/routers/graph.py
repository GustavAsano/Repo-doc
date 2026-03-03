"""
Router: /graph
Serve the dependency graph for a repository.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.state import load_repo_library, parse_library_entry_key, resolve_library_entry_assets, _normalize_language, WORKSPACE_DIR

router = APIRouter(prefix="/graph", tags=["Graph"])


@router.get("/{repo_name}", summary="Get the dependency graph for a repository")
async def get_graph(repo_name: str, language: str = "EN-US"):
    """
    Returns the nodes/edges graph JSON for a repository.
    Looks in: active workspace -> library storage.
    """
    lang = _normalize_language(language)
    library = load_repo_library()

    graph_data = None

    # 1. Try library
    for entry_key, entry in library.items():
        if not isinstance(entry, dict):
            continue
        parsed_repo, _ = parse_library_entry_key(entry_key)
        entry_repo = (entry.get("repo_name") or parsed_repo or "").strip()
        if entry_repo != repo_name:
            continue
        entry_lang = _normalize_language(entry.get("language"))
        resolved = resolve_library_entry_assets(entry_repo, entry)
        graph_path_str = resolved.get("library_graph_json") or ""
        if graph_path_str and Path(graph_path_str).exists():
            # Prefer matching language
            if entry_lang == lang:
                try:
                    graph_data = json.loads(Path(graph_path_str).read_text(encoding="utf-8"))
                    break
                except Exception:
                    pass
            elif graph_data is None:
                try:
                    graph_data = json.loads(Path(graph_path_str).read_text(encoding="utf-8"))
                except Exception:
                    pass

    if graph_data is None:
        raise HTTPException(status_code=404, detail=f"No graph found for repository '{repo_name}'.")

    return {"repo_name": repo_name, "graph": graph_data, "available": True}
