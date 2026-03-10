"""
Router: /docs
Documentation generation (technical + functional) with SSE progress streaming,
library loading, and translation.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

from app.core.state import (
    DATA_DIR,
    OUT_DIR,
    WORKSPACE_DIR,
    _normalize_language,
    activate_repo_assets,
    ensure_workspace,
    library_entry_key,
    load_functional_library,
    load_repo_library,
    parse_library_entry_key,
    reset_workspace,
    resolve_code_json,
    resolve_library_entry_assets,
    set_mkdocs_port,
    snapshot_functional_assets,
    snapshot_repo_assets,
    upsert_functional_library_entry,
    upsert_library_entry,
)
from app.schemas.repo_doc import GenerateDocRequest, GenerateFromLibraryRequest, RepoStateResponse

router = APIRouter(prefix="/docs", tags=["Documentation"])

# ---------------------------------------------------------------------------
# Generation mode constants
# ---------------------------------------------------------------------------

GEN_TECHNICAL_ONLY = "technical_only"
GEN_TECHNICAL_AND_FUNCTIONAL = "technical_and_functional"
GEN_FUNCTIONAL_ONLY = "functional_only"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sections_dict(sections: Optional[dict]) -> Optional[dict[str, dict]]:
    """Convert SectionDefinition objects to plain dicts if needed."""
    if not sections:
        return None
    return {k: (v.dict() if hasattr(v, "dict") else dict(v)) for k, v in sections.items()}


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
        print(f"[docs] MkDocs error: {err}")
        return None
    set_mkdocs_port(port)
    return port


def _graph_path_for_repo(repo_name: str, result: dict) -> Optional[str]:
    graph_file = result.get("graph_file") or str(OUT_DIR / repo_name / "graphs" / "graph.json")
    return graph_file if Path(graph_file).exists() else None


def _separate_docs(md_file: str, sections: Optional[dict], functional: bool = False) -> None:
    from app.src.doc_gen import separate_output

    if functional:
        separate_output(
            md_file,
            documentation_sections=sections,
            output_docs_dir=str(WORKSPACE_DIR / "docs_functional"),
            keep_chat_file=False,
        )
    else:
        separate_output(
            md_file,
            documentation_sections=sections,
            output_docs_dir=str(WORKSPACE_DIR / "docs"),
        )


def _default_technical_sections() -> dict:
    from app.src.doc_gen import DOCUMENTATION_SECTIONS

    return {
        k: {"title": v["title"], "description": v["description"]}
        for k, v in DOCUMENTATION_SECTIONS.items()
    }


def _default_functional_sections() -> dict:
    from app.src.doc_gen import FUNCTIONAL_DOCUMENTATION_SECTIONS

    return {
        k: {"title": v["title"], "description": v["description"]}
        for k, v in FUNCTIONAL_DOCUMENTATION_SECTIONS.items()
    }


# ---------------------------------------------------------------------------
# SSE progress streaming
# ---------------------------------------------------------------------------

async def _sse_event(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


async def _run_in_thread(fn, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))


def _make_progress_queue_callback(queue: asyncio.Queue):
    """Returns a synchronous callback that the doc_gen functions can call,
    which safely puts events onto the asyncio queue from a thread."""
    # Capture the running loop at factory time (we're in an async context here).
    # Calling asyncio.get_event_loop() from inside the worker thread fails in
    # Python 3.10+ when the thread has no loop of its own.
    loop = asyncio.get_event_loop()

    def callback(event: dict):
        try:
            asyncio.run_coroutine_threadsafe(queue.put(event), loop)
        except Exception as exc:
            print(f"[docs] progress callback error: {exc}")

    return callback


# ---------------------------------------------------------------------------
# Main generation endpoint (SSE streaming)
# ---------------------------------------------------------------------------


@router.post("/generate", summary="Generate documentation for a loaded repository (SSE stream)")
async def generate_docs(body: GenerateDocRequest):
    """
    Streams Server-Sent Events with progress updates while generating documentation.

    Event shape:
      { "event": "plan"|"call_start"|"call_end"|"done"|"error",
        "phase": str, "current_call": int, "total_calls": int, "message": str,
        "result": {...} }   <- only on "done"

    The frontend should consume this via EventSource or fetch with streaming.
    """
    ensure_workspace()

    # Resolve sections
    tech_sections = _sections_dict(body.documentation_sections) or _default_technical_sections()
    func_sections = _sections_dict(body.functional_sections) or _default_functional_sections()
    normalized_lang = _normalize_language(body.language)
    mode = body.generation_mode.lower().replace("-", "_").replace(" ", "_")

    # Locate code.json
    code_json_path = resolve_code_json(body.repo_name, preferred_language=normalized_lang)
    if code_json_path is None:
        raise HTTPException(
            status_code=404,
            detail=f"code.json not found for repository '{body.repo_name}'. Load the repository first.",
        )

    # LLM credentials
    api_key = "" if body.use_system_key else (body.api_key or "")

    async def event_stream() -> AsyncGenerator[str, None]:
        from app.src.doc_gen import (
            generate_doc,
            generate_functional_doc,
            generate_functional_doc_from_technical,
            separate_output,
        )

        queue: asyncio.Queue = asyncio.Queue()
        progress_cb = _make_progress_queue_callback(queue)
        final_result: dict[str, Any] = {}
        error_msg: Optional[str] = None

        async def run_generation():
            nonlocal error_msg
            try:
                md_file = str(WORKSPACE_DIR / "documentation.md")
                functional_md_file = str(WORKSPACE_DIR / "functional_documentation.md")
                checkpoint = str(OUT_DIR / body.repo_name / "doc_gen_resume.json")
                functional_checkpoint = str(OUT_DIR / body.repo_name / "functional_doc_gen_resume.json")

                if mode in (GEN_TECHNICAL_ONLY, GEN_TECHNICAL_AND_FUNCTIONAL):
                    await _run_in_thread(
                        generate_doc,
                        str(code_json_path),
                        md_file,
                        normalized_lang,
                        provider=body.provider,
                        model_name=body.model,
                        api_key=api_key,
                        use_system_key=body.use_system_key,
                        progress_callback=progress_cb,
                        documentation_sections=tech_sections,
                    )
                    await _run_in_thread(
                        separate_output,
                        md_file,
                        documentation_sections=tech_sections,
                        output_docs_dir=str(WORKSPACE_DIR / "docs"),
                    )
                    final_result["technical_docs"] = True

                if mode == GEN_TECHNICAL_AND_FUNCTIONAL:
                    await _run_in_thread(
                        generate_functional_doc_from_technical,
                        md_file,
                        functional_md_file,
                        normalized_lang,
                        provider=body.provider,
                        model_name=body.model,
                        api_key=api_key,
                        use_system_key=body.use_system_key,
                        progress_callback=progress_cb,
                        functional_sections=func_sections,
                        checkpoint_path=functional_checkpoint,
                    )
                    await _run_in_thread(
                        separate_output,
                        functional_md_file,
                        documentation_sections=func_sections,
                        output_docs_dir=str(WORKSPACE_DIR / "docs_functional"),
                        keep_chat_file=False,
                    )
                    final_result["functional_docs"] = True

                elif mode == GEN_FUNCTIONAL_ONLY:
                    await _run_in_thread(
                        generate_functional_doc,
                        str(code_json_path),
                        functional_md_file,
                        normalized_lang,
                        provider=body.provider,
                        model_name=body.model,
                        api_key=api_key,
                        use_system_key=body.use_system_key,
                        progress_callback=progress_cb,
                        functional_sections=func_sections,
                        checkpoint_path=str(OUT_DIR / body.repo_name / "functional_code_doc_gen_resume.json"),
                    )
                    await _run_in_thread(
                        separate_output,
                        functional_md_file,
                        documentation_sections=func_sections,
                        output_docs_dir=str(WORKSPACE_DIR / "docs_functional"),
                        keep_chat_file=False,
                    )
                    final_result["functional_docs"] = True

            except Exception as exc:
                error_msg = str(exc)
            finally:
                await queue.put(None)  # sentinel

        task = asyncio.create_task(run_generation())

        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=300)
            except asyncio.TimeoutError:
                yield await _sse_event({"event": "error", "message": "Generation timed out."})
                task.cancel()
                return

            if event is None:
                break
            yield await _sse_event(event)

        await task

        if error_msg:
            yield await _sse_event({"event": "error", "message": error_msg})
            return

        # --- Snapshot to library ---
        docs_generated = bool(final_result.get("technical_docs"))
        functional_docs_generated = bool(final_result.get("functional_docs"))
        graph_path = _graph_path_for_repo(body.repo_name, {})

        library = load_repo_library()
        source_entry = library.get(library_entry_key(body.repo_name, normalized_lang), {})

        if docs_generated or mode == GEN_TECHNICAL_AND_FUNCTIONAL:
            snap = snapshot_repo_assets(
                repo_name=body.repo_name,
                code_json_path=code_json_path,
                language=normalized_lang,
                graph_path=graph_path,
                include_functional=functional_docs_generated,
            )
            upsert_library_entry(
                body.repo_name,
                {
                    **source_entry,
                    **snap,
                    "language": normalized_lang,
                    "docs_available": bool(snap.get("docs_available")),
                    "functional_docs_available": bool(snap.get("functional_docs_available")),
                },
                language=normalized_lang,
            )

        if functional_docs_generated and mode != GEN_TECHNICAL_AND_FUNCTIONAL:
            fsnap = snapshot_functional_assets(
                repo_name=body.repo_name,
                language=normalized_lang,
                graph_path=graph_path,
                code_json_path=code_json_path,
            )
            upsert_functional_library_entry(
                body.repo_name,
                {
                    **source_entry,
                    **fsnap,
                    "language": normalized_lang,
                },
                language=normalized_lang,
            )

        # Start MkDocs
        port = _start_mkdocs(
            body.repo_name,
            repo_url=source_entry.get("repo_url"),
            author=source_entry.get("owner"),
        )

        doc_variant = (
            "functional"
            if functional_docs_generated and not docs_generated
            else "technical"
        )

        state = RepoStateResponse(
            repo_name=body.repo_name,
            language=normalized_lang,
            output_dir=str(code_json_path.parent),
            graph_path=graph_path,
            docs_generated=bool(docs_generated or functional_docs_generated),
            functional_docs_generated=functional_docs_generated,
            docs_skipped=False,
            doc_variant=doc_variant,
            generation_mode=mode,
            mkdocs_port=port,
        )

        yield await _sse_event({"event": "done", "result": state.dict()})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# Load from library + optional translation
# ---------------------------------------------------------------------------


@router.post("/load-from-library", response_model=RepoStateResponse, summary="Activate a library entry")
async def load_from_library(body: GenerateFromLibraryRequest):
    """
    Activate a saved library entry into the workspace. Optionally translate
    the documentation to the requested language in one LLM call.
    """
    ensure_workspace()
    library = load_repo_library()
    entry = library.get(body.entry_key)
    if not isinstance(entry, dict):
        raise HTTPException(status_code=404, detail="Library entry not found.")

    parsed_repo, _ = parse_library_entry_key(body.entry_key)
    repo_name = (entry.get("repo_name") or parsed_repo or "").strip()
    resolved = resolve_library_entry_assets(repo_name, entry)

    target_lang = _normalize_language(body.language)
    source_lang = _normalize_language(resolved.get("language"))
    doc_variant = "technical"

    docs_ok = activate_repo_assets(resolved, doc_variant=doc_variant)
    if not docs_ok:
        reset_workspace()

    # Translation if requested and needed
    if body.translate_on_load and source_lang != target_lang:
        from app.src.doc_gen import apply_standard_ai_disclaimer, separate_output

        try:
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import ChatPromptTemplate
            from app.src.llm_utils import init_llm

            docs_md_path = WORKSPACE_DIR / "documentation.md"
            if docs_md_path.exists():
                api_key = "" if body.use_system_key else (body.api_key or "")
                model = init_llm(
                    provider=body.provider,
                    model_name=body.model,
                    api_key=api_key,
                    use_system_key=body.use_system_key,
                )
                # Simple translation prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", f"Translate the following markdown documentation to {target_lang}. "
                               "Preserve all markdown structure, code blocks, and <!-- SECTION:X --> markers exactly."),
                    ("user", "{documentation}"),
                ])
                chain = prompt | model | StrOutputParser()
                translated = chain.invoke({"documentation": docs_md_path.read_text(encoding="utf-8")})
                translated = apply_standard_ai_disclaimer(translated, target_lang)
                docs_md_path.write_text(translated, encoding="utf-8")

                # Re-separate into individual docs
                from app.src.doc_gen import DOCUMENTATION_SECTIONS
                sections = {k: {"title": v["title"], "description": v["description"]} for k, v in DOCUMENTATION_SECTIONS.items()}
                separate_output("documentation.md", documentation_sections=sections, output_docs_dir=str(WORKSPACE_DIR / "docs"))

                # Snapshot translated version
                code_json = Path(resolved.get("library_code_json") or "")
                if code_json.exists():
                    snap = snapshot_repo_assets(
                        repo_name=repo_name,
                        code_json_path=code_json,
                        language=target_lang,
                        graph_path=resolved.get("library_graph_json"),
                    )
                    upsert_library_entry(repo_name, {**resolved, **snap, "language": target_lang}, language=target_lang)

        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Translation failed: {exc}")

    port = _start_mkdocs(repo_name, repo_url=resolved.get("repo_url"), author=resolved.get("owner"))
    graph_path = resolved.get("library_graph_json") or ""
    code_json = Path(resolved.get("library_code_json") or "")

    return RepoStateResponse(
        repo_name=repo_name,
        repo_path=resolved.get("repo_path"),
        owner=resolved.get("owner"),
        language=target_lang if body.translate_on_load else source_lang,
        output_dir=str(code_json.parent) if code_json.exists() else None,
        graph_path=graph_path if Path(graph_path).exists() else None,
        docs_generated=docs_ok,
        functional_docs_generated=bool(resolved.get("functional_docs_available")),
        docs_skipped=not docs_ok,
        doc_variant=doc_variant,
        generation_mode=body.generation_mode,
        mkdocs_port=port,
        library_entry_key=body.entry_key,
    )


# ---------------------------------------------------------------------------
# MkDocs server status
# ---------------------------------------------------------------------------


@router.get("/server", summary="Get MkDocs documentation server info")
async def get_docs_server():
    from app.core.state import get_mkdocs_port, is_port_open
    from app.src.mkdocs_ui import _resolve_docs_entry_html  # type: ignore

    port = get_mkdocs_port()
    if not port or not is_port_open(port):
        return JSONResponse(status_code=503, content={"error": "Documentation server is not running."})

    docs_dir = WORKSPACE_DIR / "docs"
    try:
        entry_html = _resolve_docs_entry_html(docs_dir)
    except Exception:
        entry_html = "index.html"

    nonce = uuid.uuid4().hex
    docs_url = f"http://127.0.0.1:{port}/{entry_html}?v={nonce}"
    return {"port": port, "docs_url": docs_url, "entry_html": entry_html}


# ---------------------------------------------------------------------------
# MkDocs reverse proxy — lets the browser reach the MkDocs server running
# inside the container via a single /docs/preview/** route on the backend.
# ---------------------------------------------------------------------------

from fastapi import Request
from fastapi.responses import Response
import httpx

@router.get("/preview/{path:path}", include_in_schema=False)
@router.get("/preview", include_in_schema=False)
async def proxy_mkdocs(request: Request, path: str = ""):
    """
    Transparent reverse-proxy to the in-process MkDocs server.
    The frontend iframe points to /docs/preview/ instead of 127.0.0.1:<port>.
    """
    from app.core.state import get_mkdocs_port, is_port_open

    port = get_mkdocs_port()
    if not port or not is_port_open(port):
        return Response(
            content="<html><body style='background:#0d1117;color:#6b7280;font-family:monospace;"
                    "display:flex;align-items:center;justify-content:center;height:100vh'>"
                    "<div>Documentation server not running. Generate docs first.</div></body></html>",
            media_type="text/html",
            status_code=503,
        )

    target_url = f"http://127.0.0.1:{port}/{path}"
    params = str(request.url.query)
    if params:
        target_url += f"?{params}"

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            resp = await client.request(
                method=request.method,
                url=target_url,
                headers={
                    k: v for k, v in request.headers.items()
                    if k.lower() not in ("host", "authorization", "content-length")
                },
                content=await request.body(),
            )
        # Rewrite absolute URLs in HTML so assets also come through the proxy
        content = resp.content
        ctype = resp.headers.get("content-type", "")
        if "text/html" in ctype:
            text = content.decode("utf-8", errors="replace")
            text = text.replace(f"http://127.0.0.1:{port}", "/docs/preview")
            text = text.replace(f"http://localhost:{port}", "/docs/preview")
            content = text.encode("utf-8")

        return Response(
            content=content,
            status_code=resp.status_code,
            media_type=ctype or None,
            headers={
                k: v for k, v in resp.headers.items()
                if k.lower() not in ("content-encoding", "transfer-encoding", "content-length")
            },
        )
    except Exception as exc:
        return Response(content=f"Proxy error: {exc}", status_code=502)
