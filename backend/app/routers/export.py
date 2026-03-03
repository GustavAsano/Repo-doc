"""
Router: /export
PDF and Word (docx) export of generated documentation.
"""

from __future__ import annotations

import base64
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.core.state import WORKSPACE_DIR, _normalize_language

router = APIRouter(prefix="/export", tags=["Export"])


def _get_md_path(repo_name: str, doc_variant: str) -> Path:
    """Return the active markdown file for the requested variant."""
    variant = str(doc_variant or "technical").strip().lower()
    if variant == "functional":
        candidates = [
            WORKSPACE_DIR / "functional_documentation.md",
            WORKSPACE_DIR / "documentation.md",
        ]
    else:
        candidates = [
            WORKSPACE_DIR / "documentation.md",
            WORKSPACE_DIR / "functional_documentation.md",
        ]
    for p in candidates:
        if p.exists():
            return p
    raise HTTPException(
        status_code=404,
        detail=f"No documentation file found in workspace for variant '{variant}'.",
    )


@router.get("/pdf/{repo_name}", summary="Export documentation as PDF")
async def export_pdf(
    repo_name: str,
    language: str = Query("EN-US"),
    doc_variant: str = Query("technical"),
):
    """
    Build and return a base64-encoded PDF of the active documentation.
    The PDF is built on-the-fly using the same fpdf2/Playwright pipeline
    as the original Streamlit app.
    """
    from app.src.doc_gen_export import build_pdf_bytes  # thin re-export shim

    md_path = _get_md_path(repo_name, doc_variant)
    lang = _normalize_language(language)
    suffix = "functional-documentation" if doc_variant == "functional" else "documentation"

    try:
        pdf_bytes = build_pdf_bytes(
            md_text=md_path.read_text(encoding="utf-8"),
            title=repo_name,
            language=lang,
            doc_kind=doc_variant,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {exc}")

    return {
        "repo_name": repo_name,
        "format": "pdf",
        "filename": f"{repo_name}-{suffix}.pdf",
        "data": base64.b64encode(pdf_bytes).decode("ascii"),
        "language": lang,
    }


@router.get("/docx/{repo_name}", summary="Export documentation as Word (.docx)")
async def export_docx(
    repo_name: str,
    language: str = Query("EN-US"),
    doc_variant: str = Query("technical"),
):
    """
    Build and return a base64-encoded Word document of the active documentation.
    """
    from app.src.doc_gen_export import build_docx_bytes

    md_path = _get_md_path(repo_name, doc_variant)
    lang = _normalize_language(language)
    suffix = "functional-documentation" if doc_variant == "functional" else "documentation"

    try:
        docx_bytes = build_docx_bytes(
            md_text=md_path.read_text(encoding="utf-8"),
            title=repo_name,
            language=lang,
            doc_kind=doc_variant,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Word export failed: {exc}")

    return {
        "repo_name": repo_name,
        "format": "docx",
        "filename": f"{repo_name}-{suffix}.docx",
        "data": base64.b64encode(docx_bytes).decode("ascii"),
        "language": lang,
    }
