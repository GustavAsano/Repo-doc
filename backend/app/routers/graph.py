"""
Router: /graph
Serve the dependency graph for a repository.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.state import (
    load_repo_library,
    parse_library_entry_key,
    resolve_library_entry_assets,
    _normalize_language,
    WORKSPACE_DIR,
    OUT_DIR,
)

router = APIRouter(prefix="/graph", tags=["Graph"])


def _try_load_graph(path: Path) -> dict | None:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None


@router.get("/{repo_name}", summary="Get the dependency graph for a repository")
async def get_graph(repo_name: str, language: str = "EN-US"):
    """
    Returns the nodes/edges graph JSON for a repository.
    Looks in: library storage (language-matched first) -> out/ workspace.
    """
    lang = _normalize_language(language)
    library = load_repo_library()

    graph_data = None

    # 1. Try library — prefer language match, fall back to any variant
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
        data = _try_load_graph(Path(graph_path_str)) if graph_path_str else None
        if data is not None:
            if entry_lang == lang:
                graph_data = data
                break
            elif graph_data is None:
                graph_data = data

    # 2. Fall back to the raw out/ workspace path produced by repo_mapping
    if graph_data is None:
        for candidate in [
            OUT_DIR / repo_name / "graphs" / "graph.json",
            OUT_DIR / repo_name / "graph.json",
        ]:
            data = _try_load_graph(candidate)
            if data is not None:
                graph_data = data
                break

    if graph_data is None:
        raise HTTPException(status_code=404, detail=f"No graph found for repository '{repo_name}'.")

    return {"repo_name": repo_name, "graph": graph_data, "available": True}
