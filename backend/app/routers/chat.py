"""
Router: /chat
Repository Q&A — asks questions against code.json + documentation.md context.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.state import (
    WORKSPACE_DIR,
    _normalize_language,
    clear_chat_history,
    load_chat_history,
    resolve_code_json,
    save_chat_history,
)
from app.schemas.repo_doc import ChatHistoryResponse, ChatMessage, ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


def _load_code_index(code_json_path: Path) -> list[dict]:
    with open(code_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = []
    for item in data:
        if item.get("ignore"):
            continue
        text = " ".join([
            item.get("path", ""),
            item.get("tipo", ""),
            item.get("nome", "") or "",
            item.get("resumo", "") or "",
        ]).lower()
        items.append({"item": item, "text": text})
    return items


def _simple_search(index: list[dict], query: str, k: int = 5) -> list[dict]:
    terms = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", query.lower())
    terms = [t for t in terms if len(t) >= 2]
    if not terms:
        return []
    scored = []
    for it in index:
        item = it["item"]
        text = it["text"]
        code = (item.get("code") or "").lower()
        name = (item.get("nome") or "").lower()
        score = 0
        for t in terms:
            score += text.count(t)
            if code:
                score += code.count(t)
            if name and t == name:
                score += 50
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [i for _, i in scored[:k]]


def _extract_doc_context(doc_md_path: Path, query: str, k: int = 5, max_chars: int = 9000) -> str:
    if not doc_md_path.exists():
        return ""
    try:
        doc_text = doc_md_path.read_text(encoding="utf-8")
    except Exception:
        return ""
    terms = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", (query or "").lower())
    terms = [t for t in terms if len(t) >= 2]
    if not terms:
        return doc_text[:max_chars]
    blocks = [b.strip() for b in re.split(r"\n\s*\n", doc_text) if b.strip()]
    scored = []
    for idx, block in enumerate(blocks):
        lower = block.lower()
        score = sum(lower.count(t) for t in terms)
        if score > 0:
            scored.append((score, -idx, block))
    if not scored:
        return doc_text[:max_chars]
    scored.sort(reverse=True)
    selected = []
    used = 0
    for _, _, block in scored[:max(1, k)]:
        extra = len(block) + (2 if selected else 0)
        if selected and used + extra > max_chars:
            break
        if not selected and len(block) > max_chars:
            selected.append(block[:max_chars])
            break
        selected.append(block)
        used += extra
    return "\n\n".join(selected)


@router.post("/message", response_model=ChatResponse, summary="Ask a question about the repository")
async def chat_message(body: ChatRequest):
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from app.src.llm_utils import init_llm

    language = _normalize_language(body.language)
    code_json_path = resolve_code_json(body.repo_name, preferred_language=language)
    if code_json_path is None:
        raise HTTPException(status_code=404, detail=f"code.json not found for '{body.repo_name}'. Generate documentation first.")

    try:
        index = _load_code_index(code_json_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load code index: {exc}")

    hits = _simple_search(index, body.question, k=5)
    doc_context = _extract_doc_context(WORKSPACE_DIR / "documentation.md", body.question, k=5, max_chars=9000)

    code_ctx = ""
    for c in hits:
        code_ctx += f"PATH: {c.get('path')}\nTYPE: {c.get('tipo')}\nNAME: {c.get('nome')}\nCODE:\n{c.get('code', '')}\n\n"
    if not code_ctx.strip():
        code_ctx = "(no code.json matches found)\n"
    if not doc_context.strip():
        doc_context = "(documentation context not available)\n"

    ctx_text = f"CODE.JSON CONTEXT (HIGH PRIORITY):\n{code_ctx}\nDOCUMENTATION.MD CONTEXT (SECONDARY):\n{doc_context}\n"

    api_key = "" if body.use_system_key else (body.api_key or "")
    try:
        model = init_llm(provider=body.provider, model_name=body.model, api_key=api_key, use_system_key=body.use_system_key, temperature=0.0)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM initialisation failed: {exc}")

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Answer in {language}. Be direct and technical. Use CODE.JSON as primary source. Use DOCUMENTATION.MD only to complement. If conflicting, follow CODE.JSON."),
        ("user", "QUESTION:\n{question}\n\nCONTEXT:\n{context}"),
    ])
    chain = prompt | model | StrOutputParser()

    try:
        answer = chain.invoke({"question": body.question, "context": ctx_text})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {exc}")

    history = load_chat_history(body.repo_name)
    history.append({"role": "user", "content": body.question})
    history.append({"role": "assistant", "content": answer})
    save_chat_history(body.repo_name, history)

    return ChatResponse(answer=answer, history=[ChatMessage(**m) for m in history])


@router.get("/history/{repo_name}", response_model=ChatHistoryResponse, summary="Get chat history for a repository")
async def get_history(repo_name: str):
    history = load_chat_history(repo_name)
    return ChatHistoryResponse(repo_name=repo_name, history=[ChatMessage(**m) for m in history])


@router.delete("/history/{repo_name}", summary="Clear chat history for a repository")
async def delete_history(repo_name: str):
    clear_chat_history(repo_name)
    return {"deleted": True, "repo_name": repo_name}
