import subprocess
import sys
import os
import re
from pathlib import Path
import yaml
import socket
import time
from urllib.parse import quote
from typing import Optional

try:
    from app.src.doc_gen import DOCUMENTATION_SECTIONS as DOC_SECTIONS
except Exception:
    DOC_SECTIONS = None

# ---------- Ordering ----------
SECTION_ORDER = [
    "index",
    "getting-started",
    "installation",
    "usage",
    "architecture",
    "technologies",
    "api-reference",
    "configuration",
    "testing",
    "file-analysis",
    "chat",
]


def normalize(name: str) -> str:
    return name.lower().replace("_", "-").strip()

def _build_section_titles() -> dict:
    if not DOC_SECTIONS:
        return {}
    titles = {}
    for key, meta in DOC_SECTIONS.items():
        slug = normalize(key)
        title = meta.get("title")
        if title:
            titles[slug] = title
    return titles


SECTION_TITLES = _build_section_titles()

_MKDOCS_PROCESS: Optional[subprocess.Popen] = None
_MKDOCS_PORT: int | None = None


def title_from_filename(name: str) -> str:
    norm = normalize(name)
    if norm in SECTION_TITLES:
        return SECTION_TITLES[norm]
    return name.replace("-", " ").replace("_", " ").title()


def _read_first_heading(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("<!--"):
            continue
        if line.startswith("# "):
            return line[2:].strip() or None
    return None


def title_from_doc_path(path: Path, fallback_name: str) -> str:
    heading = _read_first_heading(path)
    if heading:
        heading = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", heading).strip()
        if heading:
            return heading
    return title_from_filename(fallback_name)


def _heading_number_tokens(path: Path) -> tuple[int, ...] | None:
    heading = _read_first_heading(path)
    if not heading:
        return None
    match = re.match(r"^\s*(\d+(?:\.\d+)*)\.?\s+", heading)
    if not match:
        return None
    try:
        return tuple(int(token) for token in match.group(1).split("."))
    except Exception:
        return None


def _extra_nav_sort_key(slug: str, path: Path) -> tuple:
    number_tokens = _heading_number_tokens(path)
    if number_tokens is not None:
        return (0, number_tokens, normalize(slug))
    return (1, normalize(slug))

def order_key(path: Path) -> tuple:
    name = normalize(path.stem)
    if name == "index":
        return (0, "")

    try:
        return (SECTION_ORDER.index(name) + 1, "")
    except ValueError:
        return (len(SECTION_ORDER) + 1, name)


def build_nav(docs_dir: Path):
    nav = []

    sorted_files = sorted(docs_dir.glob("*.md"), key=lambda p: normalize(p.stem))
    files = {p.stem.lower().replace("_", "-"): p for p in sorted_files}
    dirs = {p.name.lower().replace("_", "-"): p for p in docs_dir.iterdir() if p.is_dir()}

    if "index" in files:
        nav.append({title_from_doc_path(files["index"], "index"): "index.md"})

    def add_section(section: str):
        if section in files:
            nav.append({
                title_from_doc_path(files[section], section): files[section].name
            })

        elif section in dirs:
            index_md = dirs[section] / "index.md"
            if index_md.exists():
                nav.append({
                    title_from_filename(section): [
                        {title_from_doc_path(index_md, "index"): f"{section}/index.md"}
                    ]
                })

    for section in SECTION_ORDER:
        if section in ("index", "chat"):
            continue

        add_section(section)

    used = set(SECTION_ORDER)
    extras = [
        (key, path)
        for key, path in files.items()
        if key not in used and path.name != "index.md"
    ]
    extras.sort(key=lambda item: _extra_nav_sort_key(item[0], item[1]))
    for key, path in extras:
        if key not in used and path.name != "index.md":
            nav.append({title_from_doc_path(path, key): path.name})

    if "chat" in files or "chat" in dirs:
        add_section("chat")

    return nav


# ---------- Index bootstrap ----------
def create_index_md(docs_dir: Path, repo_name: str):
    index_path = docs_dir / "index.md"
    if index_path.exists():
        return

    # If repository documentation already has section files, do not force-create a default Overview.
    for md_file in docs_dir.glob("*.md"):
        if md_file.name.lower() not in {"index.md", "chat.md"}:
            return

    index_path.write_text(
        f"# {repo_name}\n\n"
        "## Overview\n"
        "This documentation was automatically generated.\n\n"
        "Use the navigation menu to explore the repository structure and usage.\n",
        encoding="utf-8"
    )


def create_chat_md(docs_dir: Path, repo_name: str):
    chat_path = docs_dir / "chat.md"
    repo_q = quote(repo_name)
    iframe = (
        "<div class=\"chat-page\">\n"
        f"<iframe src=\"http://127.0.0.1:8501/?view=chat&repo={repo_q}\"></iframe>\n"
        "</div>\n"
    )
    if chat_path.exists():
        try:
            existing = chat_path.read_text(encoding="utf-8")
            if iframe in existing:
                return
        except Exception:
            pass
    chat_path.write_text(iframe, encoding="utf-8")


def ensure_extra_css(docs_dir: Path):
    css_path = docs_dir / "extra.css"
    css_content = (
        "@media screen and (min-width: 76.25em) {\n"
        "  .md-tabs {\n"
        "    position: sticky;\n"
        "    top: 2.4rem;\n"
        "    z-index: 3;\n"
        "  }\n"
        "  .md-tabs[hidden] {\n"
        "    pointer-events: auto;\n"
        "  }\n"
        "  .md-tabs[hidden] .md-tabs__link {\n"
        "    opacity: 0.7;\n"
        "    transform: none;\n"
        "  }\n"
        "  .md-tabs[hidden] .md-tabs__item--active .md-tabs__link {\n"
        "    opacity: 1;\n"
        "  }\n"
        "}\n"
        "html { scroll-padding-top: 5rem; }\n"
        ".chat-page {\n"
        "  position: relative;\n"
        "  left: 50%;\n"
        "  right: 50%;\n"
        "  margin-left: -50vw;\n"
        "  margin-right: -50vw;\n"
        "  width: 100vw;\n"
        "  height: calc(100vh - 64px);\n"
        "  min-height: 640px;\n"
        "  margin-top: -64px;\n"
        "  padding-bottom: 0;\n"
        "}\n"
        ".chat-page iframe {\n"
        "  width: 100%;\n"
        "  height: 100%;\n"
        "  border: 0;\n"
        "}\n"
        ".md-content__inner:has(.chat-page) {padding-top: 0;}\n"
        ".md-content__inner:has(.chat-page) > h1 {display: none;}\n"
        ".md-content__inner:has(.chat-page) > p {display: none;}\n"
        ".md-content__inner:has(.chat-page) {margin: 0;}\n"
        ".md-content__inner:has(.chat-page) > .chat-page {margin-top: -64px;}\n"
    )
    css_path.write_text(css_content, encoding="utf-8")


# ---------- MkDocs generation ----------
def generate_mkdocs_config(
    project_root: Path,
    repo_name: str,
    repo_url: str | None = None,
    author: str | None = None,
    site_language: str | None = None,
):
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    create_index_md(docs_dir, repo_name)
    create_chat_md(docs_dir, repo_name)
    ensure_extra_css(docs_dir)
    nav = build_nav(docs_dir)

    # Normalize site language (e.g., PT-BR -> pt)
    site_lang = (site_language or "en").split("-")[0].lower()

    # Sanitiza repo_url: só aceita URLs com esquema http/https
    if repo_url and not (repo_url.startswith("http://") or repo_url.startswith("https://")):
        repo_url = None

    mkdocs_config = {
        "site_name": f"{repo_name} Documentation",
        "site_description": f"Technical documentation for the {repo_name} repository",
        "site_author": author or "Unknown",
        "repo_name": repo_name,
        "docs_dir": "docs",
        "site_dir": "site",
        "use_directory_urls": False,
        "theme": {
            "name": "material",
            "language": site_lang,
            "features": [
                "navigation.tabs",
                "navigation.sections",
                "navigation.top",
                "search.highlight",
                "content.code.copy",
            ],
        },
        "nav": nav,
        "plugins": ["search"],
        "extra_css": ["extra.css"],
        "markdown_extensions": [
            "admonition",
            "pymdownx.superfences",
            "pymdownx.details",
            {
                "pymdownx.tasklist": {
                    "custom_checkbox": True
                }
            },
            "pymdownx.highlight",
            "pymdownx.inlinehilite",
            "pymdownx.magiclink",
            "pymdownx.extra",
            {
                "toc": {
                    "permalink": True
                }
            },
        ],
    }

    if repo_url:
        mkdocs_config["repo_url"] = repo_url

    with open(project_root / "mkdocs.yml", "w", encoding="utf-8") as f:
        yaml.safe_dump(mkdocs_config, f, sort_keys=False)



def _first_nav_doc_path(nav_node) -> str | None:
    if isinstance(nav_node, str):
        return nav_node.strip() or None
    if isinstance(nav_node, list):
        for item in nav_node:
            found = _first_nav_doc_path(item)
            if found:
                return found
        return None
    if isinstance(nav_node, dict):
        for value in nav_node.values():
            found = _first_nav_doc_path(value)
            if found:
                return found
        return None
    return None


def _resolve_docs_entry_html(docs_dir: Path) -> str:
    mkdocs_config_path = docs_dir.parent / "mkdocs.yml"
    try:
        if mkdocs_config_path.exists():
            with open(mkdocs_config_path, encoding="utf-8") as f:
                mkdocs_config = yaml.safe_load(f) or {}
            nav_first_doc = _first_nav_doc_path(mkdocs_config.get("nav"))
            if nav_first_doc:
                nav_doc_path = Path(str(nav_first_doc).strip())
                if nav_doc_path.suffix.lower() == ".md" and nav_doc_path.name.lower() != "chat.md":
                    if (docs_dir / nav_doc_path.name).exists():
                        return f"{nav_doc_path.stem}.html"
    except Exception:
        pass
    if (docs_dir / "index.md").exists():
        return "index.html"
    try:
        md_candidates = sorted(
            [p for p in docs_dir.glob("*.md") if p.name.lower() != "chat.md"],
            key=lambda p: p.name.lower(),
        )
        if md_candidates:
            return f"{md_candidates[0].stem}.html"
    except Exception:
        pass
    return "index.html"


def _is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def find_free_port(start: int = 8000, end: int = 8100) -> int:
    for port in range(start, end):
        if _is_port_free(port):
            return port
    raise RuntimeError("No free port available")


def _stop_mkdocs_process() -> None:
    global _MKDOCS_PROCESS, _MKDOCS_PORT
    proc = _MKDOCS_PROCESS
    if not proc:
        return
    try:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except Exception:
                proc.kill()
    except Exception:
        pass
    _MKDOCS_PROCESS = None
    _MKDOCS_PORT = None


def serve_mkdocs(
    project_root: Path,
    port: int | None = None,
    force_restart: bool = False,
) -> tuple[int | None, str | None]:
    global _MKDOCS_PROCESS, _MKDOCS_PORT

    if force_restart:
        _stop_mkdocs_process()

    if _MKDOCS_PROCESS and _MKDOCS_PROCESS.poll() is None and _MKDOCS_PORT:
        return _MKDOCS_PORT, None

    if _MKDOCS_PROCESS and _MKDOCS_PROCESS.poll() is not None:
        _MKDOCS_PROCESS = None
        _MKDOCS_PORT = None

    if port is None:
        port = find_free_port()

    log_path = project_root / "mkdocs_serve.log"
    env = os.environ.copy()
    # Force UTF-8 to avoid Windows cp1252 crashes from third-party plugin warnings.
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    with open(log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "mkdocs",
                "serve",
                "--dev-addr",
                f"127.0.0.1:{port}",
            ],
            cwd=project_root,
            stdout=log_file,
            stderr=log_file,
            env=env,
        )

    # espera curta para detectar falha imediata
    time.sleep(1.5)
    if proc.poll() is not None:
        try:
            return None, log_path.read_text(encoding="utf-8")
        except Exception:
            return None, "mkdocs failed to start. Check mkdocs_serve.log"

    _MKDOCS_PROCESS = proc
    _MKDOCS_PORT = port
    return port, None

