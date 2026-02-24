DOCUMENTATION_SECTIONS = {
    "INDEX": {
        "title": "Overview",
        "description": "Describe repository purpose, target audience, and key capabilities."
    },
    "GETTING_STARTED": {
        "title": "Getting Started",
        "description": "Quick steps to run the project for the first time."
    },
    "INSTALLATION": {
        "title": "Installation",
        "description": "System requirements, dependencies, and detailed setup steps."
    },
    "USAGE": {
        "title": "Usage",
        "description": "Practical usage flows, examples, and common scenarios."
    },
    "ARCHITECTURE": {
        "title": "Architecture",
        "description": "Architecture overview, folder structure, main modules, and responsibilities."
    },
    "TECHNOLOGIES": {
        "title": "Technologies",
        "description": "Main technologies, frameworks, libraries, and tools."
    },
    "API_REFERENCE": {
        "title": "API Reference",
        "description": "Functions, classes, methods, and public interfaces."
    },
    "CONFIGURATION": {
        "title": "Configuration",
        "description": "Configuration files, environment variables, and adjustable parameters."
    },
    "TESTING": {
        "title": "Testing",
        "description": "How to run tests, available test types, and best practices."
    },
    "FILE_ANALYSIS": {
        "title": "File-by-File Analysis",
        "description": "Detailed analysis of each file with responsibilities, dependencies, and behavior."
    }
}
FUNCTIONAL_DOCUMENTATION_SECTIONS = {
    "OVERVIEW": {
        "title": "Overview",
        "description": "Summarize business context, objective, and expected outcomes of the solution."
    },
    "BUSINESS_SCOPE": {
        "title": "Business Scope",
        "description": "Define business boundaries, stakeholders, responsibilities, and covered domains/processes."
    },
    "FUNCTIONAL_FLOWS": {
        "title": "Functional Flows",
        "description": "Describe end-to-end functional flows, inputs, outputs, and decision points."
    },
    "BUSINESS_RULES_EXCEPTIONS": {
        "title": "Business Rules and Exceptions",
        "description": "List applicable business rules, validations, constraints, and exception scenarios."
    },
    "OPERATIONAL_PROCEDURES": {
        "title": "Operational Procedures",
        "description": "Describe operational routines, monitoring points, manual procedures, and support actions."
    },
}
SECTION_STYLE_RULES = {
    "INDEX": {
        "min_paragraphs": 3,
        "max_bullets": 0,
        "guidance": "Narrative-only overview. Do not use bullet lists in this section.",
    },
    "GETTING_STARTED": {
        "min_paragraphs": 1,
        "max_bullets": None,
        "guidance": "Allow concise actionable steps, but keep context in prose.",
    },
    "INSTALLATION": {
        "min_paragraphs": 2,
        "max_bullets": None,
        "guidance": "Explain setup rationale and dependencies in prose before listing commands.",
    },
    "USAGE": {
        "min_paragraphs": 2,
        "max_bullets": 4,
        "guidance": "Describe usage flows and component interaction in prose; keep examples concise.",
    },
    "ARCHITECTURE": {
        "min_paragraphs": 2,
        "max_bullets": 4,
        "guidance": "Prioritize module interaction narrative over itemized catalogs.",
    },
    "TECHNOLOGIES": {
        "min_paragraphs": 2,
        "max_bullets": 4,
        "guidance": "Explain why each technology is used; avoid pure laundry-list style.",
    },
    "API_REFERENCE": {
        "min_paragraphs": 2,
        "max_bullets": 6,
        "guidance": "Summarize API surface in prose and reserve bullets for key classes/functions.",
    },
    "CONFIGURATION": {
        "min_paragraphs": 2,
        "max_bullets": 4,
        "guidance": "Group config concerns with explanatory prose plus focused bullet lists.",
    },
    "TESTING": {
        "min_paragraphs": 2,
        "max_bullets": 4,
        "guidance": "Describe test strategy in prose; keep command lists short.",
    },
    "FILE_ANALYSIS": {
        "min_paragraphs": 1,
        "max_bullets": None,
        "guidance": "Bullets are acceptable, but include synthesis paragraph(s) about file groups.",
    },
}
FUNCTIONAL_SECTION_STYLE_RULES = {
    "OVERVIEW": {
        "min_paragraphs": 2,
        "max_bullets": 2,
        "guidance": "High-level business narrative with concise contextual bullets only when necessary.",
    },
    "BUSINESS_SCOPE": {
        "min_paragraphs": 2,
        "max_bullets": 4,
        "guidance": "Clarify boundaries, actors, ownership, and process coverage in business terms.",
    },
    "FUNCTIONAL_FLOWS": {
        "min_paragraphs": 2,
        "max_bullets": None,
        "guidance": "Prioritize clear step-by-step functional behavior and transitions between states.",
    },
    "BUSINESS_RULES_EXCEPTIONS": {
        "min_paragraphs": 1,
        "max_bullets": None,
        "guidance": "Rules and exception handling can use structured lists for precision and readability.",
    },
    "OPERATIONAL_PROCEDURES": {
        "min_paragraphs": 2,
        "max_bullets": 6,
        "guidance": "Focus on operation, support, and continuity procedures, with practical sequencing.",
    },
}

DEFAULT_CONTEXT_WINDOW_TOKENS = 800_000
DEFAULT_PROMPT_OVERHEAD_TOKENS = 12_000
DEFAULT_OUTPUT_RESERVE_TOKENS = 24_000
DEFAULT_MIN_CHUNK_TOKENS = 120_000
DEFAULT_MAX_TOTAL_TOKENS = 10_000_000
DEFAULT_MAX_LLM_CALLS = 120
DEFAULT_OPENAI_REQUEST_TOKEN_CAP = 120_000
DEFAULT_OPENAI_MODEL_REQUEST_CAPS = {
    "gpt-5-nano": 120_000,
    "gpt-5-mini": 120_000,
    "gpt-4o-mini": 120_000,
    "gpt-4o": 120_000,
}
DEFAULT_BEDROCK_REQUEST_TOKEN_CAP = 120_000
DEFAULT_BEDROCK_MODEL_REQUEST_CAPS = {
    # Moonshot models on Bedrock currently expose 262,144 context tokens.
    # Keep a buffer for prompt overhead/output reserve.
    "moonshot.kimi-k2-thinking": 240_000,
    "moonshotai.kimi-k2.5": 240_000,
}
DEFAULT_OPENAI_TPM_CAP = 180_000
DEFAULT_OPENAI_MODEL_TPM_CAPS = {
    "gpt-5-nano": 180_000,
    "gpt-5-mini": 180_000,
    "gpt-4o-mini": 180_000,
    "gpt-4o": 180_000,
}
DEFAULT_EVIDENCE_ITEMS_PER_SECTION_PER_CHUNK = 10
DEFAULT_EVIDENCE_ITEMS_PER_SECTION_TOTAL = 48
DEFAULT_EVIDENCE_REFS_PER_ITEM = 6
PENDING_MARKER = "[PENDING]"
INTERMEDIATE_MARKERS = [
    "[PENDING]",
    "[pendente]",
    "[EVIDENCIA NOVA]",
    "[EVIDÊNCIA NOVA]",
    "[evidencia nova]",
    "[evidência nova]",
    "[NEW EVIDENCE]",
    "[new evidence]",
]
META_PROCESS_PATTERNS = [
    r"\bchunk\b",
    r"\bneste\s+chunk\b",
    r"\bchunk\s+atual\b",
    r"\btrecho\s+do\s+repositorio\b",
    r"\bevidence\s+pack\b",
    r"\bpack\s+de\s+evid[eê]ncias\b",
    r"\bevid[eê]ncia\s+nova\b",
    r"\bevid[eê]ncias?\s+extra[ií]das?\b",
]
DOC_META_LINE_PATTERNS = [
    r"^\s*[-*]?\s*observa[cç][aã]o(?:\s+de|\s+sobre)?\b",
    r"^\s*[-*]?\s*nota(?:s)?\b",
    r"^\s*[-*]?\s*limita[cç][oõ]es?\s+de\s+evid[eê]ncia\b",
    r"\bpontos?\s+de\s+evid[eê]ncia\b",
    r"\bevid[eê]ncia:\b",
    r"\bevidence:\b",
    r"^\s*evidence\b",
    r"^\s*evid[eê]ncias?\b",
    r"\bcom\s+evid[eê]ncia\b",
    r"\brecomenda-se\s+consultar\b",
    r"\bpara\s+detalhes\s+operacionais,\s*consulte\b",
    r"\bcaso\s+seja\s+necess[aá]rio\b.*\bconsultar\b",
    r"\bse\s+(?:quiser|desejar)\b",
    r"\bif\s+you\s+(?:want|need)\b",
]
STANDARD_AI_DISCLAIMER_BY_LANG = {
    "PT-BR": (
        "> **Aviso (IA):** Este conteúdo foi gerado automaticamente por IA a partir dos artefatos do "
        "repositório e pode conter imprecisões. Valide decisões críticas diretamente no código-fonte."
    ),
    "EN-US": (
        "> **AI Notice:** This content was automatically generated by AI from repository artifacts and may "
        "contain inaccuracies. Validate critical decisions directly in the source code."
    ),
    "ES-ES": (
        "> **Aviso de IA:** Este contenido fue generado automáticamente por IA a partir de artefactos del "
        "repositorio y puede contener imprecisiones. Valide las decisiones críticas directamente en el código fuente."
    ),
    "FR-FR": (
        "> **Avis IA :** Ce contenu a été généré automatiquement par IA à partir des artefacts du dépôt et "
        "peut contenir des imprécisions. Validez les décisions critiques directement dans le code source."
    ),
    "DE-DE": (
        "> **KI-Hinweis:** Dieser Inhalt wurde automatisch durch KI aus Repository-Artefakten erzeugt und "
        "kann Ungenauigkeiten enthalten. Validieren Sie kritische Entscheidungen direkt im Quellcode."
    ),
}
AI_DISCLAIMER_VARIANT_PATTERNS = [
    r"\bai[- ]generated\b",
    r"\bai\s+notice\b",
    r"\bgenerated\s+by\s+ai\b",
    r"\bcontent\s+was\s+automatically\s+generated\s+by\s+ai\b",
    r"\baviso\s*\(\s*ia\s*\)\b",
    r"\bconte[uú]do\s+foi\s+gerad[oa].*por\s+ia\b",
    r"\baviso\s+de\s+conte[uú]do\s+gerado\s+por\s+ia\b",
    r"\bcontenido\s+fue\s+generad[oa].*por\s+ia\b",
    r"\baviso\s+de\s+ia\b",
    r"\bcontenu\s+a\s+[ée]t[ée]\s+g[ée]n[ée]r[ée].*par\s+ia\b",
    r"\bavis\s+ia\b",
    r"\bki[- ]hinweis\b",
    r"\bdurch\s+ki\s+.*erzeugt\b",
    r"\bvon\s+ki\s+erstellt\b",
]


def _default_documentation_sections(default_sections=None):
    sections_map = (
        default_sections
        if isinstance(default_sections, dict) and default_sections
        else DOCUMENTATION_SECTIONS
    )
    return {
        key: {
            "title": str(meta.get("title") or key).strip(),
            "description": str(meta.get("description") or "").strip(),
        }
        for key, meta in sections_map.items()
    }


def _coerce_runtime_sections(custom_sections=None, default_sections=None):
    import re
    import unicodedata

    sections_map = (
        default_sections
        if isinstance(default_sections, dict) and default_sections
        else DOCUMENTATION_SECTIONS
    )

    if custom_sections is None:
        return _default_documentation_sections(default_sections=sections_map)

    if isinstance(custom_sections, dict):
        rows = []
        for key, value in custom_sections.items():
            if isinstance(value, dict):
                rows.append(
                    {
                        "key": key,
                        "title": value.get("title"),
                        "description": value.get("description"),
                    }
                )
    elif isinstance(custom_sections, list):
        rows = list(custom_sections)
    else:
        raise ValueError("documentation_sections must be a dict or list when provided.")

    def _norm_key(value):
        raw = str(value or "").strip()
        raw = unicodedata.normalize("NFKD", raw)
        raw = "".join(ch for ch in raw if not unicodedata.combining(ch))
        key = raw.upper().replace("-", "_").replace(" ", "_")
        key = re.sub(r"[^A-Z0-9_]", "", key)
        return key

    normalized = {}
    used = set()
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"Invalid section definition at position {idx}.")
        title = str(row.get("title") or row.get("name") or "").strip()
        description = str(row.get("description") or "").strip()
        if not title or not description:
            raise ValueError(
                f"Each section must include non-empty title and description (row {idx})."
            )

        raw_key = row.get("key") or title
        key = _norm_key(raw_key)
        if not key:
            key = f"SECTION_{idx}"
        base = key
        suffix = 2
        while key in used:
            key = f"{base}_{suffix}"
            suffix += 1
        used.add(key)
        normalized[key] = {"title": title, "description": description}

    if not normalized:
        raise ValueError("At least one documentation section is required.")
    return normalized


def _active_sections(sections=None, default_sections=None):
    fallback_sections = (
        default_sections
        if isinstance(default_sections, dict) and default_sections
        else DOCUMENTATION_SECTIONS
    )
    return sections if isinstance(sections, dict) and sections else fallback_sections


def _normalize_doc_language(language):
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


def _language_meta(language):
    lang = _normalize_doc_language(language)
    by_lang = {
        "PT-BR": {
            "name": "Português (Brasil)",
            "strict_rule": "Escreva EXCLUSIVAMENTE em Português (Brasil). Nunca escreva em outro idioma.",
        },
        "EN-US": {
            "name": "English (US)",
            "strict_rule": "Write EXCLUSIVELY in English (US). Never switch to another language.",
        },
        "ES-ES": {
            "name": "Español (España)",
            "strict_rule": "Escribe EXCLUSIVAMENTE en Español (España). Nunca cambies a otro idioma.",
        },
        "FR-FR": {
            "name": "Français (France)",
            "strict_rule": "Rédige EXCLUSIVEMENT en Français (France). N'utilise jamais une autre langue.",
        },
        "DE-DE": {
            "name": "Deutsch (Deutschland)",
            "strict_rule": "Schreibe AUSSCHLIESSLICH auf Deutsch (Deutschland). Nutze keine andere Sprache.",
        },
    }
    return by_lang.get(lang, by_lang["EN-US"])


def _localized_standard_section_titles(language):
    lang = _normalize_doc_language(language)
    base = {
        key: str(meta.get("title") or key)
        for key, meta in DOCUMENTATION_SECTIONS.items()
    }
    localized_by_lang = {
        "PT-BR": {
            "INDEX": "Visão Geral",
            "GETTING_STARTED": "Primeiros Passos",
            "INSTALLATION": "Instalação",
            "USAGE": "Uso",
            "ARCHITECTURE": "Arquitetura",
            "TECHNOLOGIES": "Tecnologias",
            "API_REFERENCE": "Referência de API",
            "CONFIGURATION": "Configuração",
            "TESTING": "Testes",
            "FILE_ANALYSIS": "Análise Arquivo a Arquivo",
        },
        "EN-US": {},
        "ES-ES": {
            "INDEX": "Descripción General",
            "GETTING_STARTED": "Primeros Pasos",
            "INSTALLATION": "Instalación",
            "USAGE": "Uso",
            "ARCHITECTURE": "Arquitectura",
            "TECHNOLOGIES": "Tecnologías",
            "API_REFERENCE": "Referencia de API",
            "CONFIGURATION": "Configuración",
            "TESTING": "Pruebas",
            "FILE_ANALYSIS": "Análisis Archivo por Archivo",
        },
        "FR-FR": {
            "INDEX": "Vue d'ensemble",
            "GETTING_STARTED": "Prise en Main",
            "INSTALLATION": "Installation",
            "USAGE": "Utilisation",
            "ARCHITECTURE": "Architecture",
            "TECHNOLOGIES": "Technologies",
            "API_REFERENCE": "Référence API",
            "CONFIGURATION": "Configuration",
            "TESTING": "Tests",
            "FILE_ANALYSIS": "Analyse Fichier par Fichier",
        },
        "DE-DE": {
            "INDEX": "Überblick",
            "GETTING_STARTED": "Erste Schritte",
            "INSTALLATION": "Installation",
            "USAGE": "Nutzung",
            "ARCHITECTURE": "Architektur",
            "TECHNOLOGIES": "Technologien",
            "API_REFERENCE": "API-Referenz",
            "CONFIGURATION": "Konfiguration",
            "TESTING": "Tests",
            "FILE_ANALYSIS": "Datei-für-Datei-Analyse",
        },
    }
    out = dict(base)
    out.update(localized_by_lang.get(lang, {}))
    return out


def _localized_standard_functional_section_titles(language):
    lang = _normalize_doc_language(language)
    base = {
        key: str(meta.get("title") or key)
        for key, meta in FUNCTIONAL_DOCUMENTATION_SECTIONS.items()
    }
    localized_by_lang = {
        "PT-BR": {
            "OVERVIEW": "Visão Geral",
            "BUSINESS_SCOPE": "Escopo de Negócio",
            "FUNCTIONAL_FLOWS": "Fluxos Funcionais",
            "BUSINESS_RULES_EXCEPTIONS": "Regras de Negócio e Exceções",
            "OPERATIONAL_PROCEDURES": "Procedimentos Operacionais",
        },
        "EN-US": {},
        "ES-ES": {
            "OVERVIEW": "Descripción General",
            "BUSINESS_SCOPE": "Alcance de Negocio",
            "FUNCTIONAL_FLOWS": "Flujos Funcionales",
            "BUSINESS_RULES_EXCEPTIONS": "Reglas de Negocio y Excepciones",
            "OPERATIONAL_PROCEDURES": "Procedimientos Operativos",
        },
        "FR-FR": {
            "OVERVIEW": "Vue d'ensemble",
            "BUSINESS_SCOPE": "Périmètre Métier",
            "FUNCTIONAL_FLOWS": "Flux Fonctionnels",
            "BUSINESS_RULES_EXCEPTIONS": "Règles Métier et Exceptions",
            "OPERATIONAL_PROCEDURES": "Procédures Opérationnelles",
        },
        "DE-DE": {
            "OVERVIEW": "Überblick",
            "BUSINESS_SCOPE": "Geschäftsumfang",
            "FUNCTIONAL_FLOWS": "Funktionale Abläufe",
            "BUSINESS_RULES_EXCEPTIONS": "Geschäftsregeln und Ausnahmen",
            "OPERATIONAL_PROCEDURES": "Betriebliche Verfahren",
        },
    }
    out = dict(base)
    out.update(localized_by_lang.get(lang, {}))
    return out


def _rewrite_section_titles_by_map(documentation_md, title_map):
    import re

    text = str(documentation_md or "")
    if not text.strip():
        return text
    if not isinstance(title_map, dict) or not title_map:
        return text

    marker_re = re.compile(r"^\s*<!--\s*SECTION:([A-Z_]+)\s*-->\s*$")
    lines = text.splitlines()

    for idx, line in enumerate(lines):
        match = marker_re.match(line.strip())
        if not match:
            continue
        section_key = match.group(1).strip().upper()
        target_title = title_map.get(section_key)
        if not target_title:
            continue
        j = idx + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and lines[j].lstrip().startswith("# "):
            indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
            current_heading = lines[j].lstrip()[2:].strip()
            prefix_match = re.match(r"^(\d+(?:\.\d+)*\.?)\s+(.+)$", current_heading)
            number_prefix = f"{prefix_match.group(1)} " if prefix_match else ""
            lines[j] = f"{indent}# {number_prefix}{target_title}"
    return "\n".join(lines)


def _rewrite_standard_section_titles(documentation_md, language):
    return _rewrite_section_titles_by_map(
        documentation_md=documentation_md,
        title_map=_localized_standard_section_titles(language),
    )


def _rewrite_standard_functional_section_titles(documentation_md, language):
    return _rewrite_section_titles_by_map(
        documentation_md=documentation_md,
        title_map=_localized_standard_functional_section_titles(language),
    )


def _unique_keep_order(values, limit=30):
    out = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        out.append(value)
        if len(out) >= limit:
            break
    return out


def _extract_notebook_markdown_titles(text):
    import re

    titles = []
    in_markdown_cell = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## Markdown Cell "):
            in_markdown_cell = True
            continue
        if line.startswith("## Code Cell ") or line.startswith("## Notebook Metadata"):
            in_markdown_cell = False
            continue
        if not in_markdown_cell:
            continue
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if match:
            titles.append(match.group(1).strip())
    return titles


def _build_repo_evidence_snapshot(file_payloads):
    import re

    notebook_count = 0
    file_paths = []
    tables = []
    variables = []
    imports = []
    notebook_titles = []

    table_pattern = re.compile(r"""spark\.table\(\s*['"]([^'"]+)['"]\s*\)""")
    var_pattern = re.compile(r"""^\s*([A-Za-z_]\w*)\s*=\s*.+$""", re.MULTILINE)
    import_pattern = re.compile(
        r"""^\s*(?:from\s+([A-Za-z_][\w\.]*)\s+import|import\s+([A-Za-z_][\w\.]*))""",
        re.MULTILINE,
    )

    for item in file_payloads:
        path = item.get("path", "")
        code = item.get("code", "")
        file_paths.append(path)
        if path.lower().endswith(".ipynb"):
            notebook_count += 1

        tables.extend(table_pattern.findall(code))
        variables.extend(var_pattern.findall(code))
        for g1, g2 in import_pattern.findall(code):
            imports.append(g1 or g2)
        if path.lower().endswith(".ipynb") or "## Markdown Cell " in code:
            notebook_titles.extend(_extract_notebook_markdown_titles(code))

    paths_short = _unique_keep_order(file_paths, limit=10)
    tables_short = _unique_keep_order(tables, limit=20)
    vars_short = _unique_keep_order(variables, limit=30)
    imports_short = _unique_keep_order(imports, limit=20)
    titles_short = _unique_keep_order(notebook_titles, limit=25)

    lines = [
        f"- Files considered: {len(file_paths)}",
        f"- Notebook files: {notebook_count}",
        f"- Main files: {', '.join(paths_short) if paths_short else 'N/A'}",
        f"- Notebook markdown titles detected: {', '.join(titles_short) if titles_short else 'N/A'}",
        f"- Spark tables detected: {', '.join(tables_short) if tables_short else 'N/A'}",
        f"- Main variables/dataframes detected: {', '.join(vars_short) if vars_short else 'N/A'}",
        f"- Imports/packages detected: {', '.join(imports_short) if imports_short else 'N/A'}",
    ]
    return "\n".join(lines)


def _notebook_text_from_raw_json(raw_text):
    """Converte conteúdo bruto de .ipynb (JSON em string) para texto legível."""
    import json

    try:
        notebook = json.loads(raw_text)
    except Exception:
        return ""

    cells = notebook.get("cells", []) if isinstance(notebook, dict) else []
    if not isinstance(cells, list):
        return ""

    parts = []
    for idx, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            continue
        cell_type = (cell.get("cell_type") or "").strip().lower()
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(str(x) for x in source)
        elif source is None:
            source = ""
        else:
            source = str(source)
        source = source.strip()
        if not source:
            continue

        if cell_type == "markdown":
            parts.append(f"## Markdown Cell {idx}\n{source}")
        elif cell_type == "code":
            parts.append(f"## Code Cell {idx}\n{source}")

    text = "\n\n".join(parts).strip()
    if len(text) > 200_000:
        text = text[:200_000] + "\n\n...[notebook truncated]..."
    return text


def _approx_tokens_text(text):
    if not text:
        return 0
    return max(1, len(text) // 4)


def _normalize_path(path):
    return str(path or "").replace("\\", "/")


def _folder_of(path):
    normalized = _normalize_path(path)
    if "/" in normalized:
        return normalized.rsplit("/", 1)[0]
    return ""


def _priority_key(item):
    priority = item.get("priority")
    if isinstance(priority, int) and priority > 0:
        return priority
    return 10**15


def _resolve_request_token_cap(provider, model_name, request_token_cap):
    if request_token_cap is not None:
        cap = int(request_token_cap)
        if cap <= 0:
            raise ValueError("request_token_cap must be positive when provided.")
        return cap

    provider_norm = (provider or "").strip().lower()
    model_norm = (model_name or "").strip().lower()
    if provider_norm == "openai":
        for known_model, cap in DEFAULT_OPENAI_MODEL_REQUEST_CAPS.items():
            if known_model in model_norm:
                return int(cap)
        return int(DEFAULT_OPENAI_REQUEST_TOKEN_CAP)
    if provider_norm == "bedrock":
        for known_model, cap in DEFAULT_BEDROCK_MODEL_REQUEST_CAPS.items():
            if known_model in model_norm:
                return int(cap)
        return int(DEFAULT_BEDROCK_REQUEST_TOKEN_CAP)
    return None


def _resolve_tpm_limit(provider, model_name, tpm_limit_tokens):
    if tpm_limit_tokens is not None:
        cap = int(tpm_limit_tokens)
        if cap <= 0:
            raise ValueError("tpm_limit_tokens must be positive when provided.")
        return cap

    provider_norm = (provider or "").strip().lower()
    model_norm = (model_name or "").strip().lower()
    if provider_norm == "openai":
        for known_model, cap in DEFAULT_OPENAI_MODEL_TPM_CAPS.items():
            if known_model in model_norm:
                return int(cap)
        return int(DEFAULT_OPENAI_TPM_CAP)
    return None


def _build_sections_format(sections=None):
    sections_map = _active_sections(sections)
    sections_format = ""
    for key, section in sections_map.items():
        sections_format += (
            f"<!-- SECTION:{key} -->\n"
            f"# {section['title']}\n"
            f"(Write section content for: {section['description']})\n\n"
        )
    return sections_format


def _escape_prompt_literal(text):
    value = str(text or "")
    return value.replace("{", "{{").replace("}", "}}")


def _build_sections_brief(sections=None):
    sections_map = _active_sections(sections)
    lines = []
    for key, section in sections_map.items():
        lines.append(f"- {key}: {section['title']} -> {section['description']}")
    return "\n".join(lines)


def _build_section_style_guide(sections=None, style_rules=None):
    sections_map = _active_sections(sections)
    active_rules = (
        style_rules
        if isinstance(style_rules, dict) and style_rules
        else SECTION_STYLE_RULES
    )
    lines = []
    for key, section in sections_map.items():
        rule = active_rules.get(key, {})
        min_paragraphs = int(rule.get("min_paragraphs", 1))
        max_bullets_raw = rule.get("max_bullets", 6)
        guidance = str(rule.get("guidance", "")).strip()
        if max_bullets_raw is None:
            base = (
                f"- {key} ({section['title']}): at least {min_paragraphs} prose paragraph(s); "
                "no hard maximum for bullet items."
            )
        else:
            max_bullets = max(0, int(max_bullets_raw))
            base = (
                f"- {key} ({section['title']}): at least {min_paragraphs} prose paragraph(s); "
                f"at most {max_bullets} bullet item(s)."
            )
        if guidance:
            base += f" {guidance}"
        lines.append(base)
    return "\n".join(lines)


def _section_style_target_line(section_key, sections=None, style_rules=None):
    sections_map = _active_sections(sections)
    section = sections_map.get(section_key, {"title": section_key})
    active_rules = (
        style_rules
        if isinstance(style_rules, dict) and style_rules
        else SECTION_STYLE_RULES
    )
    rule = active_rules.get(section_key, {})
    min_paragraphs = int(rule.get("min_paragraphs", 1))
    max_bullets_raw = rule.get("max_bullets", 6)
    guidance = str(rule.get("guidance", "")).strip()
    if max_bullets_raw is None:
        line = (
            f"{section_key} ({section['title']}): at least {min_paragraphs} prose paragraph(s); "
            "no hard maximum for bullet items."
        )
    else:
        max_bullets = max(0, int(max_bullets_raw))
        line = (
            f"{section_key} ({section['title']}): at least {min_paragraphs} prose paragraph(s); "
            f"at most {max_bullets} bullet item(s)."
        )
    if guidance:
        line += f" {guidance}"
    return line


def _parse_document_sections(text):
    import re

    marker_re = re.compile(r"^\s*<!--\s*SECTION:([A-Z_]+)\s*-->\s*$")
    lines = str(text or "").splitlines()
    sections = {}
    order = []
    current_key = None
    current_lines = []

    for line in lines:
        match = marker_re.match(line.strip())
        if match:
            if current_key is not None:
                sections[current_key] = list(current_lines)
            current_key = match.group(1).strip()
            if current_key not in order:
                order.append(current_key)
            current_lines = [line]
            continue

        if current_key is not None:
            current_lines.append(line)

    if current_key is not None:
        sections[current_key] = list(current_lines)

    return sections, order


def _section_body_text(section_lines):
    import re

    lines = list(section_lines or [])
    if not lines:
        return ""
    content = []
    for line in lines[1:]:
        stripped = line.strip()
        if re.match(r"^#\s+", stripped):
            continue
        content.append(line)
    return "\n".join(content).strip()


def _incomplete_required_sections(text, min_chars=20, sections=None):
    sections_map = _active_sections(sections)
    sections, _ = _parse_document_sections(text)
    missing = []
    for key in sections_map.keys():
        lines = sections.get(key)
        if not lines:
            missing.append(key)
            continue
        body = _section_body_text(lines)
        normalized = " ".join(body.split())
        if len(normalized) < int(min_chars):
            missing.append(key)
    return missing


def _ensure_required_sections_skeleton(text, sections=None):
    sections_map = _active_sections(sections)
    sections, _ = _parse_document_sections(text)
    output = []
    for key, section in sections_map.items():
        existing = sections.get(key)
        if existing:
            output.extend(existing)
        else:
            output.append(f"<!-- SECTION:{key} -->")
            output.append(f"# {section['title']}")
            output.append("")
        output.append("")
    return "\n".join(output).strip() + "\n"


def _missing_section_fallback_line(language):
    lang = _normalize_doc_language(language)
    by_lang = {
        "PT-BR": "Não foram identificados detalhes explícitos suficientes para esta seção nos artefatos disponíveis do repositório.",
        "EN-US": "Sufficient explicit details for this section were not identified in the available repository artifacts.",
        "ES-ES": "No se identificaron detalles explícitos suficientes para esta sección en los artefactos disponibles del repositorio.",
        "FR-FR": "Les artefacts disponibles du dépôt ne fournissent pas suffisamment de détails explicites pour cette section.",
        "DE-DE": "In den verfügbaren Repository-Artefakten wurden für diesen Abschnitt keine ausreichenden expliziten Details gefunden.",
    }
    return by_lang.get(lang, by_lang["EN-US"])


def _fill_incomplete_sections_with_fallback(text, language, min_chars=40, sections=None):
    sections_map = _active_sections(sections)
    sections, _ = _parse_document_sections(text)
    fallback = _missing_section_fallback_line(language)
    output = []
    for key, section in sections_map.items():
        lines = list(sections.get(key) or [])
        if not lines:
            lines = [f"<!-- SECTION:{key} -->", f"# {section['title']}", "", fallback]
        else:
            body = _section_body_text(lines)
            normalized = " ".join(body.split())
            if len(normalized) < int(min_chars):
                # Preserve marker/title and append neutral fallback line.
                lines = list(lines)
                if lines and lines[-1].strip():
                    lines.append("")
                lines.append(fallback)
        output.extend(lines)
        output.append("")
    return "\n".join(output).strip() + "\n"


def _coerce_generated_section(raw_text, section_key, language, min_chars=20, sections=None):
    sections_map = _active_sections(sections)
    section = sections_map.get(section_key, {"title": section_key})
    parsed_sections, parsed_order = _parse_document_sections(raw_text)
    chosen_lines = list(parsed_sections.get(section_key) or [])

    body = ""
    if chosen_lines:
        body = _section_body_text(chosen_lines)
    elif parsed_order:
        first_key = parsed_order[0]
        body = _section_body_text(parsed_sections.get(first_key) or [])
    else:
        cleaned = []
        for line in str(raw_text or "").splitlines():
            stripped = line.strip()
            if stripped.startswith("<!-- SECTION:"):
                continue
            if stripped.startswith("# "):
                continue
            cleaned.append(line)
        body = "\n".join(cleaned).strip()

    normalized = " ".join(str(body or "").split())
    if len(normalized) < int(min_chars):
        body = _missing_section_fallback_line(language)

    lines = [
        f"<!-- SECTION:{section_key} -->",
        f"# {section['title']}",
        "",
        str(body or "").strip(),
    ]
    return "\n".join(lines).strip()


def _assemble_document_from_sections(section_outputs, language, sections=None):
    sections_map = _active_sections(sections)
    blocks = []
    for key in sections_map.keys():
        raw_section = section_outputs.get(key, "")
        blocks.append(_coerce_generated_section(raw_section, key, language, sections=sections_map))
    return "\n\n".join(blocks).strip() + "\n"


def _collect_file_payloads(lista_repositorio):
    file_payloads = []
    for idx, arquivo in enumerate(lista_repositorio):
        if arquivo.get("tipo") != "file":
            continue

        ignore = bool(arquivo.get("ignore"))
        ignored_before_conversion = ignore
        path = str(arquivo.get("path", ""))
        code_text = arquivo.get("code", "")

        # Fallback: aceita .ipynb ignorado quando veio em JSON bruto no code.json.
        if ignore and path.lower().endswith(".ipynb"):
            converted = _notebook_text_from_raw_json(code_text)
            if converted:
                code_text = converted
                ignore = False

        if ignore:
            continue

        approx_tokens = arquivo.get("tokens_aprox", 0)
        if (
            not isinstance(approx_tokens, int)
            or approx_tokens <= 0
            or (ignored_before_conversion and path.lower().endswith(".ipynb"))
        ):
            approx_tokens = _approx_tokens_text(code_text)

        file_payloads.append(
            {
                "path": path,
                "code": code_text,
                "tokens": max(1, int(approx_tokens)),
                "priority": arquivo.get("priority"),
                "orig_index": idx,
                "folder": _folder_of(path),
            }
        )
    return file_payloads


def _sort_files_for_doc(file_payloads):
    return sorted(file_payloads, key=lambda item: (_priority_key(item), item.get("orig_index", 0)))


def _split_text_by_chars(text, max_chars):
    if not text:
        return [""]
    if max_chars <= 0:
        return [text]
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def _split_text_into_token_chunks(text, token_budget):
    import re

    raw_text = str(text or "")
    if not raw_text.strip():
        return []

    token_budget = max(1, int(token_budget))
    paragraphs = re.split(r"\n\s*\n", raw_text)
    chunks = []
    current = []
    current_tokens = 0
    max_chars_for_forced = max(1024, token_budget * 4)

    for paragraph in paragraphs:
        piece = paragraph.strip()
        if not piece:
            continue
        piece_tokens = _approx_tokens_text(piece)
        if piece_tokens > token_budget:
            if current:
                chunks.append("\n\n".join(current).strip())
                current = []
                current_tokens = 0
            forced_parts = _split_text_by_chars(piece, max_chars_for_forced)
            for forced in forced_parts:
                forced_clean = str(forced or "").strip()
                if forced_clean:
                    chunks.append(forced_clean)
            continue
        if current and (current_tokens + piece_tokens > token_budget):
            chunks.append("\n\n".join(current).strip())
            current = [piece]
            current_tokens = piece_tokens
        else:
            current.append(piece)
            current_tokens += piece_tokens

    if current:
        chunks.append("\n\n".join(current).strip())

    return [chunk for chunk in chunks if chunk]


def _split_large_file(file_payload, token_budget):
    token_budget = max(1, int(token_budget))
    if int(file_payload.get("tokens", 0)) <= token_budget:
        return [file_payload]

    code = file_payload.get("code", "") or ""
    lines = code.splitlines(keepends=True)
    if not lines:
        lines = [code]

    max_chars_per_piece = max(512, token_budget * 4)
    raw_parts = []
    current_lines = []
    current_tokens = 0

    for line in lines:
        line_tokens = _approx_tokens_text(line)
        if line_tokens > token_budget:
            if current_lines:
                raw_parts.append("".join(current_lines))
                current_lines = []
                current_tokens = 0
            raw_parts.extend(_split_text_by_chars(line, max_chars_per_piece))
            continue

        if current_lines and (current_tokens + line_tokens > token_budget):
            raw_parts.append("".join(current_lines))
            current_lines = [line]
            current_tokens = line_tokens
        else:
            current_lines.append(line)
            current_tokens += line_tokens

    if current_lines:
        raw_parts.append("".join(current_lines))
    if not raw_parts:
        raw_parts = _split_text_by_chars(code, max_chars_per_piece)

    total_parts = len(raw_parts)
    out = []
    for part_idx, part_code in enumerate(raw_parts, start=1):
        part = dict(file_payload)
        part["path"] = f"{file_payload.get('path', '')} [part {part_idx}/{total_parts}]"
        part["code"] = part_code
        part["tokens"] = _approx_tokens_text(part_code)
        out.append(part)
    return out


def _ensure_current_item_fits_budget(files, cursor, token_budget):
    if cursor >= len(files):
        return files
    token_budget = max(1, int(token_budget))
    current = files[cursor]
    current_tokens = int(current.get("tokens", 0) or 0)
    if current_tokens <= token_budget:
        return files
    parts = _split_large_file(current, token_budget)
    return files[:cursor] + parts + files[cursor + 1:]


def _take_next_chunk(files, start_idx, token_budget, min_chunk_tokens):
    if start_idx >= len(files):
        return [], start_idx, 0

    token_budget = max(1, int(token_budget))
    min_chunk_tokens = max(1, int(min_chunk_tokens))

    end = start_idx
    total = 0
    while end < len(files):
        item_tokens = max(1, int(files[end].get("tokens", 0) or 1))
        if end > start_idx and (total + item_tokens > token_budget):
            break
        total += item_tokens
        end += 1

    if end == start_idx:
        end = min(start_idx + 1, len(files))
        total = max(1, int(files[start_idx].get("tokens", 0) or 1))

    # Prefer cut at folder boundary when chunk stays reasonably dense.
    if end < len(files):
        running_tokens = 0
        best_cut = None
        fallback_cut = None
        for idx in range(start_idx, end - 1):
            running_tokens += max(1, int(files[idx].get("tokens", 0) or 1))
            cut_idx = idx + 1
            if files[idx].get("folder") != files[cut_idx].get("folder"):
                fallback_cut = (cut_idx, running_tokens)
                if running_tokens >= min_chunk_tokens:
                    best_cut = (cut_idx, running_tokens)
        chosen = best_cut or fallback_cut
        if chosen is not None:
            cut_idx, cut_tokens = chosen
            return files[start_idx:cut_idx], cut_idx, cut_tokens

    return files[start_idx:end], end, total


def _estimate_initial_multi_pass_calls(files, token_budget, min_chunk_tokens, max_llm_calls):
    if token_budget <= 0:
        return 1
    queue = list(files)
    cursor = 0
    calls = 0
    while cursor < len(queue):
        queue = _ensure_current_item_fits_budget(queue, cursor, token_budget)
        effective_min = min_chunk_tokens if min_chunk_tokens <= token_budget else max(1, token_budget // 2)
        chunk_items, next_cursor, _ = _take_next_chunk(
            queue,
            start_idx=cursor,
            token_budget=token_budget,
            min_chunk_tokens=effective_min,
        )
        if not chunk_items or next_cursor <= cursor:
            break
        calls += 1
        cursor = next_cursor
        if calls >= max_llm_calls:
            break
    return max(1, calls)


def _render_repo_content(file_payloads):
    chunks = []
    for payload in file_payloads:
        path = payload.get("path", "")
        code = payload.get("code", "")
        chunks.append(f"PATH DO ARQUIVO: {path}\nCONTEUDO DO ARQUIVO:\n{code}\n")
    return "\n".join(chunks).strip()


def _empty_evidence_pack(sections=None):
    sections_map = _active_sections(sections)
    return {key: [] for key in sections_map.keys()}


def _canonical_evidence_key(text):
    import re

    value = str(text or "").strip().lower()
    if not value:
        return ""
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^a-z0-9_./\\ -]+", "", value)
    return value[:240]


def _normalize_evidence_refs(values, limit=DEFAULT_EVIDENCE_REFS_PER_ITEM):
    refs = []
    for value in values or []:
        raw = str(value or "").strip()
        if not raw:
            continue
        refs.append(raw)
    return _unique_keep_order(refs, limit=limit)


def _coerce_section_item(raw):
    if isinstance(raw, dict):
        statement = (
            raw.get("statement")
            or raw.get("fact")
            or raw.get("text")
            or raw.get("item")
            or ""
        )
        evidence = raw.get("evidence") or raw.get("references") or raw.get("refs") or raw.get("files") or []
    else:
        statement = raw
        evidence = []

    statement = str(statement or "").strip()
    if not statement:
        return None
    if _is_meta_process_statement(statement):
        return None

    if isinstance(evidence, str):
        evidence = [evidence]
    elif not isinstance(evidence, list):
        evidence = [str(evidence)]

    return {
        "statement": statement,
        "evidence": _normalize_evidence_refs(evidence, limit=DEFAULT_EVIDENCE_REFS_PER_ITEM),
    }


def _is_meta_process_statement(text):
    import re

    value = str(text or "").strip().lower()
    if not value:
        return False
    for pattern in META_PROCESS_PATTERNS:
        if re.search(pattern, value, flags=re.IGNORECASE):
            return True
    return False


def _is_doc_meta_line(text):
    import re

    value = str(text or "").strip()
    if not value:
        return False
    for pattern in DOC_META_LINE_PATTERNS:
        if re.search(pattern, value, flags=re.IGNORECASE):
            return True
    return False


def _extract_json_object(raw_text):
    import json

    text = str(raw_text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            return None
    return None


def _normalize_section_key(value):
    import re

    key = str(value or "").strip().upper().replace("-", "_").replace(" ", "_")
    key = re.sub(r"[^A-Z0-9_]", "", key)
    return key


def _parse_chunk_evidence_response(raw_text, sections=None):
    sections_map = _active_sections(sections)
    parsed = _extract_json_object(raw_text)
    pack = _empty_evidence_pack(sections=sections_map)
    if not isinstance(parsed, dict):
        return pack

    section_payload = parsed.get("sections")
    if isinstance(section_payload, dict):
        source = section_payload
    else:
        source = parsed

    normalized = {}
    for key, value in source.items():
        normalized[_normalize_section_key(key)] = value

    for section_key in sections_map.keys():
        raw_items = normalized.get(section_key)
        if raw_items is None:
            continue
        if not isinstance(raw_items, list):
            raw_items = [raw_items]
        for raw_item in raw_items:
            item = _coerce_section_item(raw_item)
            if item is not None:
                pack[section_key].append(item)
    return pack


def _merge_evidence_packs(
    current,
    incoming,
    max_items_per_section=DEFAULT_EVIDENCE_ITEMS_PER_SECTION_TOTAL,
    sections=None,
):
    sections_map = _active_sections(sections)
    merged = _empty_evidence_pack(sections=sections_map)
    max_items_per_section = max(1, int(max_items_per_section))

    for section_key in sections_map.keys():
        section_items = []
        key_to_index = {}

        def _add(item):
            coerced = _coerce_section_item(item)
            if coerced is None:
                return
            canonical = _canonical_evidence_key(coerced.get("statement", ""))
            if not canonical:
                return
            if canonical in key_to_index:
                idx = key_to_index[canonical]
                refs = (section_items[idx].get("evidence") or []) + (coerced.get("evidence") or [])
                section_items[idx]["evidence"] = _normalize_evidence_refs(
                    refs,
                    limit=DEFAULT_EVIDENCE_REFS_PER_ITEM,
                )
                return
            if len(section_items) >= max_items_per_section:
                return
            key_to_index[canonical] = len(section_items)
            section_items.append(
                {
                    "statement": coerced.get("statement", "").strip(),
                    "evidence": _normalize_evidence_refs(
                        coerced.get("evidence") or [],
                        limit=DEFAULT_EVIDENCE_REFS_PER_ITEM,
                    ),
                }
            )

        for src in (current.get(section_key, []) if isinstance(current, dict) else []):
            _add(src)
        for src in (incoming.get(section_key, []) if isinstance(incoming, dict) else []):
            _add(src)

        merged[section_key] = section_items

    return merged


def _render_consolidated_evidence_pack(
    pack,
    max_items_per_section=DEFAULT_EVIDENCE_ITEMS_PER_SECTION_TOTAL,
    sections=None,
):
    sections_map = _active_sections(sections)
    max_items_per_section = max(1, int(max_items_per_section))
    lines = []
    for section_key, section in sections_map.items():
        lines.append(f"## SECTION:{section_key} - {section['title']}")
        items = list(pack.get(section_key, []))[:max_items_per_section]
        if not items:
            lines.append("- No concrete evidence extracted for this section yet.")
            lines.append("")
            continue
        for item in items:
            statement = str(item.get("statement", "")).strip()
            if not statement:
                continue
            refs = _normalize_evidence_refs(item.get("evidence") or [], limit=DEFAULT_EVIDENCE_REFS_PER_ITEM)
            if refs:
                lines.append(f"- {statement} (evidence: {', '.join(refs)})")
            else:
                lines.append(f"- {statement}")
        lines.append("")
    return "\n".join(lines).strip()


def _fit_consolidated_evidence_to_budget(pack, budget_tokens, global_summary_tokens, sections=None):
    budget_tokens = max(1, int(budget_tokens))
    global_summary_tokens = max(0, int(global_summary_tokens))
    max_items = int(DEFAULT_EVIDENCE_ITEMS_PER_SECTION_TOTAL)

    while max_items >= 1:
        rendered = _render_consolidated_evidence_pack(
            pack,
            max_items_per_section=max_items,
            sections=sections,
        )
        rendered_tokens = _approx_tokens_text(rendered)
        if rendered_tokens + global_summary_tokens <= budget_tokens:
            return rendered, max_items, rendered_tokens
        if max_items == 1:
            break
        max_items = max(1, int(max_items * 0.75))

    rendered = _render_consolidated_evidence_pack(
        pack,
        max_items_per_section=1,
        sections=sections,
    )
    return rendered, 1, _approx_tokens_text(rendered)


def _build_doc_prompt(
    lang_meta,
    sections_format,
    pass_index,
    is_multi_pass,
    has_previous_doc,
    is_final,
    sections=None,
):
    from langchain_core.prompts import ChatPromptTemplate

    section_style_guide = _escape_prompt_literal(_build_section_style_guide(sections=sections))
    stage_rules = []
    if is_multi_pass:
        stage_rules.append("- This is a chunked pass. Keep coherence and avoid partial-process language.")
    if is_final:
        stage_rules.append("- Return a polished final version with consistent style across sections.")

    stage_text = "\n".join(stage_rules).strip()
    if stage_text:
        stage_text = _escape_prompt_literal(f"\n\nMULTI-PASS RULES:\n{stage_text}\n")

    sections_format_escaped = _escape_prompt_literal(sections_format)

    system_text = f"""
            You are a senior software engineer writing technical repository documentation.

            Repository input format:
            - PATH DO ARQUIVO: file path
            - CONTEUDO DO ARQUIVO: file content

            Your task is to write high-quality technical documentation from repository evidence.
            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}
            {stage_text}
            DEPTH REQUIREMENTS:
            - Avoid generic text.
            - Cite concrete evidence: file names, variables, tables, functions, steps, metrics.
            - Prefer specific evidence over broad statements.
            - If evidence is missing, state that explicitly; do not invent facts.
            - For notebooks, describe logical flow (objective, ingestion, cleaning, joins, aggregations, metrics, outputs).
            - Keep section-level coherence and avoid disconnected topical fragments.
            - Prefer concise paragraphs; use bullets only when they add clarity.
            - Start each section with at least one short contextual paragraph before optional bullets.
            - Expand technical depth by explaining interactions, trade-offs, and behavior from existing evidence.
            - Avoid repeated templates such as multiple "Observação ..." entries.
            - Do NOT write custom AI-generation disclaimers; a standard disclaimer is injected automatically.

            MANDATORY RULES:
            - Write ONLY inside the sections.
            - Use EXACTLY the section delimiters below.
            - Do NOT change section titles.
            - Do NOT write text outside sections.
            - Do NOT add extra sections.
            - Never output process/meta tags such as [EVIDENCIA NOVA], [NEW EVIDENCE], [TODO].

            SECTION STYLE TARGETS:
            {section_style_guide}

            Required output format:

            {sections_format_escaped}
            """

    if has_previous_doc:
        user_text = (
            "DOCUMENTACAO_ATUAL:\n{documentacao_atual}\n\n"
            "EVIDENCIAS EXTRAIDAS:\n{evidencias}\n\n"
            "NOVO TRECHO DO REPOSITORIO:\n\n{conteudo_repositorio}"
        )
    else:
        user_text = "EVIDENCIAS EXTRAIDAS:\n{evidencias}\n\nREPOSITORIO:\n\n{conteudo_repositorio}"

    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_chunk_evidence_prompt(lang_meta, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    sections_map = _active_sections(sections)
    sections_brief = _escape_prompt_literal(_build_sections_brief(sections=sections_map))
    evidence_schema_lines = []
    for section_key in sections_map.keys():
        evidence_schema_lines.append(
            f'  "{section_key}": [{{"statement":"...", "evidence":["path/a.py","path/b.md"]}}]'
        )
    evidence_schema = _escape_prompt_literal("{\n" + ",\n".join(evidence_schema_lines) + "\n}")
    system_text = f"""
            You are a senior software engineer extracting technical repository evidence.

            Target language for statements: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            TASK:
            - Analyze the repository chunk and produce a structured evidence pack.
            - Extract only concrete facts that are explicitly supported by the chunk content.
            - Include file paths, APIs, classes, functions, commands, config keys, tests, and behaviors when available.
            - Avoid generic statements and avoid process language.
            - Do NOT write statements like "this chunk does not contain ..." or "the chunk emphasizes ...".
            - If a section has no concrete evidence in the current chunk, return an empty list for that section.
            - Do not write documentation prose yet.

            OUTPUT FORMAT (STRICT JSON, no markdown):
            {evidence_schema}

            RULES:
            - Return valid JSON only.
            - Use each section key exactly as defined above.
            - Up to {DEFAULT_EVIDENCE_ITEMS_PER_SECTION_PER_CHUNK} items per section.
            - Keep each statement concise and technical.
            - Evidence list should reference concrete file paths from the chunk when possible.
            - Never mention chunking process, extraction process, or intermediate workflow.

            SECTION GUIDE:
            {sections_brief}
            """
    user_text = (
        "EVIDENCIAS RESUMIDAS DO CHUNK:\n{chunk_evidence}\n\n"
        "CHUNK DO REPOSITORIO:\n{chunk_content}"
    )
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_functional_chunk_evidence_prompt(lang_meta, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    sections_map = _active_sections(
        sections,
        default_sections=FUNCTIONAL_DOCUMENTATION_SECTIONS,
    )
    sections_brief = _escape_prompt_literal(
        _build_sections_brief(
            sections=sections_map,
        )
    )
    section_style_guide = _escape_prompt_literal(
        _build_section_style_guide(
            sections=sections_map,
            style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
        )
    )
    evidence_schema_lines = []
    for section_key in sections_map.keys():
        evidence_schema_lines.append(
            f'  "{section_key}": [{{"statement":"...", "evidence":["path/a.py","path/b.md"]}}]'
        )
    evidence_schema = _escape_prompt_literal("{\n" + ",\n".join(evidence_schema_lines) + "\n}")
    system_text = f"""
            You are a principal business analyst extracting functional repository evidence from source-code chunks.

            Target language for statements: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            TASK:
            - Analyze the repository chunk and produce a structured functional evidence pack.
            - Extract only concrete facts explicitly supported by the chunk content.
            - Prioritize business purpose, user/actor actions, process flow, decision points, rules, exceptions, operational routines, and outcomes.
            - Include file paths as evidence references whenever possible.
            - Avoid deep implementation details unless they are necessary to explain functional behavior.
            - Do NOT write final documentation prose yet.
            - Do NOT write statements like "this chunk does not contain ..." or meta-comments about chunk emphasis.
            - If a section has no concrete evidence in this chunk, return an empty list for that section.

            OUTPUT FORMAT (STRICT JSON, no markdown):
            {evidence_schema}

            RULES:
            - Return valid JSON only.
            - Use each section key exactly as defined above.
            - Up to {DEFAULT_EVIDENCE_ITEMS_PER_SECTION_PER_CHUNK} items per section.
            - Keep each statement concise, factual, and functionally oriented.
            - Evidence list should reference concrete file paths from the chunk when possible.
            - Never mention chunking process, extraction process, or intermediate workflow.

            SECTION GUIDE:
            {sections_brief}

            SECTION STYLE TARGETS (for downstream writing):
            {section_style_guide}
            """
    user_text = (
        "CHUNK SUMMARY (RAW FACT HINTS):\n{chunk_evidence}\n\n"
        "REPOSITORY CHUNK:\n{chunk_content}"
    )
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_final_doc_from_evidence_prompt(lang_meta, sections_format, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    section_style_guide = _escape_prompt_literal(_build_section_style_guide(sections=sections))
    sections_format_escaped = _escape_prompt_literal(sections_format)
    system_text = f"""
            You are a principal engineer writing a final technical repository documentation.

            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            INPUT:
            - Consolidated evidence extracted from all repository chunks.
            - Global repository summary.

            OBJECTIVE:
            - Produce one coherent, high-quality final documentation.
            - Integrate evidence from all sections without "stitched" artifacts.

            WRITING RULES:
            - Keep section-level narrative coherence.
            - Prefer concise paragraphs and use bullets only when they add clear structure.
            - Start each section with at least one short contextual paragraph before optional bullets.
            - Avoid repetitive templates and duplicated facts.
            - Never mention process steps such as "new evidence", "chunk", "pending", "see below", extraction, or similar.
            - Do NOT include labels like "Observação", "Nota", "Observação de evidência", or "Limitações de evidência".
            - Do NOT mention "evidence/evidência" as a writing meta-comment; present facts directly.
            - Use impersonal technical tone; avoid second-person address such as "se quiser", "você pode", "if you want".
            - Do NOT write recommendation filler such as "recomenda-se consultar..." or generic "consulte o código-fonte".
            - Do NOT write custom AI-generation disclaimers; a standard disclaimer is injected automatically.
            - Never encode lists inline with " - " inside one paragraph; when enumerating 3+ items, use proper markdown bullets.
            - Expand technical depth by connecting components, data flow, and responsibilities from provided evidence.
            - If evidence is insufficient for a specific point, state the limitation directly and cleanly.
            - Keep technical depth with explicit file/path evidence where relevant.

            HARD CONSTRAINTS:
            - Write ONLY inside the required sections.
            - Keep exact section delimiters and titles.
            - Do NOT add or remove sections.
            - Every required section must be present exactly once and non-empty.
            - Do NOT invent facts.

            SECTION STYLE TARGETS:
            {section_style_guide}

            Required output format:

            {sections_format_escaped}
            """
    user_text = (
        "GLOBAL SUMMARY:\n{global_summary}\n\n"
        "CONSOLIDATED EVIDENCE PACK:\n{consolidated_evidence}"
    )
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_section_doc_from_context_prompt(lang_meta, section_key, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    sections_map = _active_sections(sections)
    section = sections_map.get(section_key)
    if section is None:
        raise ValueError(f"Unknown documentation section key: {section_key}")

    section_style_target = _escape_prompt_literal(
        _section_style_target_line(section_key, sections=sections_map)
    )
    required_format = (
        f"<!-- SECTION:{section_key} -->\n"
        f"# {section['title']}\n"
        "(Write only this section content)\n"
    )
    required_format_escaped = _escape_prompt_literal(required_format)
    section_title_escaped = _escape_prompt_literal(section["title"])
    system_text = f"""
            You are a principal engineer writing one technical documentation section.

            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            OBJECTIVE:
            - Write only the requested section with deep technical detail.
            - Use only facts present in the provided context and summary.
            - Keep coherent prose and use bullets when they improve structure.

            RULES:
            - Output exactly one section: {section_key} ({section_title_escaped}).
            - Do not output any other section marker or title.
            - Do not mention chunking, evidence extraction process, pending items, or "new evidence".
            - Do not include labels like "Observação", "Nota", "Observação de evidência", or "Limitações de evidência".
            - Do not add custom AI-generation disclaimers.
            - Use impersonal technical tone; avoid second-person address.
            - Do not invent facts.
            - If information is insufficient, state this cleanly inside the section.

            SECTION STYLE TARGET:
            - {section_style_target}

            Required output format:
            {required_format_escaped}
            """
    user_text = (
        "GLOBAL SUMMARY:\n{global_summary}\n\n"
        "CONTEXT FOR WRITING:\n{section_context}"
    )
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_final_cleanup_prompt(lang_meta, sections_format, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    section_style_guide = _escape_prompt_literal(_build_section_style_guide(sections=sections))
    marker_examples = _escape_prompt_literal(", ".join(INTERMEDIATE_MARKERS))
    sections_format_escaped = _escape_prompt_literal(sections_format)
    system_text = f"""
            You are a senior software engineer finalizing repository documentation.

            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            Your task: rewrite the full documentation into a coherent final version.

            FINALIZATION RULES:
            - You have editorial freedom to improve fluency, coherence, and organization.
            - You may reorder, merge, or split paragraphs and bullets inside each section.
            - You may switch bullets <-> prose when it improves readability and structure.
            - Preserve all section delimiters and exact section titles from the required format.
            - Keep every required section present exactly once and non-empty.
            - Remove temporary workflow markers and stage labels, including: {marker_examples}.
            - Remove references like "new evidence added", "pending", "to be completed", or similar process text.
            - Remove commentary labels such as "Observação", "Nota", "Observação de evidência", "Limitações de evidência".
            - Remove meta-writing mentions of "evidence/evidência"; write the technical facts directly.
            - Use impersonal technical tone; avoid second-person address (e.g., "se quiser", "if you want").
            - Remove generic recommendation filler such as "recomenda-se consultar..." and "para detalhes..., consulte...".
            - Remove any custom AI-generation disclaimers; the final output must keep only the standard disclaimer.
            - Convert inline pseudo-lists ("texto - item - item - item") into proper markdown bullets when needed.
            - Convert short explanatory bullet blocks (1-2 long bullets) into compact prose paragraphs when listing is unnecessary.
            - Remove broken references like "see below" when no direct continuation exists.
            - Remove duplicated bullets/sentences and collapse repetitive topical fragments.
            - If evidence is still missing, state it as a clean factual limitation (without tags).
            - Keep technical depth and concrete evidence.
            - Resolve style inconsistencies and contradictions across sections.
            - FACT FIDELITY IS MANDATORY: do not add any new facts, entities, versions, paths, commands, metrics, or claims.
            - Only reorganize and rephrase information already present in DOCUMENTACAO_ATUAL.
            - You may also use SUPPORTING_EVIDENCE only to enrich detail that is already represented there; never add external facts.
            - If unsure about a detail, remove it instead of inventing.
            - Do not add sections.

            SECTION STYLE TARGETS:
            {section_style_guide}

            Required output format:

            {sections_format_escaped}
            """
    user_text = (
        "SUPPORTING_EVIDENCE:\n{supporting_evidence}\n\n"
        "DOCUMENTACAO_ATUAL:\n{documentacao_atual}"
    )
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _coerce_cost_usd(value):
    try:
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip().replace("$", "")
        amount = float(value)
        if amount < 0:
            return None
        return amount
    except Exception:
        return None


def _extract_response_cost_usd(response, model=None):
    from collections import deque

    def _is_scalar(value):
        return isinstance(value, (str, bytes, int, float, bool))

    def _extract_tokens_mapping(data):
        if not isinstance(data, dict):
            return None, None
        prompt_keys = (
            "prompt_tokens",
            "input_tokens",
            "promptTokenCount",
            "inputTokenCount",
        )
        completion_keys = (
            "completion_tokens",
            "output_tokens",
            "completionTokenCount",
            "outputTokenCount",
        )

        prompt_tokens = None
        completion_tokens = None
        for key in prompt_keys:
            value = data.get(key)
            try:
                if value is not None:
                    prompt_tokens = int(value)
                    break
            except Exception:
                continue
        for key in completion_keys:
            value = data.get(key)
            try:
                if value is not None:
                    completion_tokens = int(value)
                    break
            except Exception:
                continue
        return prompt_tokens, completion_tokens

    def _extract_tokens(response_obj):
        usage = getattr(response_obj, "usage_metadata", None)
        prompt_tokens, completion_tokens = _extract_tokens_mapping(usage)
        if prompt_tokens is not None or completion_tokens is not None:
            return prompt_tokens, completion_tokens

        metadata = getattr(response_obj, "response_metadata", None)
        if isinstance(metadata, dict):
            for key in ("token_usage", "usage"):
                prompt_tokens, completion_tokens = _extract_tokens_mapping(metadata.get(key))
                if prompt_tokens is not None or completion_tokens is not None:
                    return prompt_tokens, completion_tokens
            prompt_tokens, completion_tokens = _extract_tokens_mapping(metadata)
            if prompt_tokens is not None or completion_tokens is not None:
                return prompt_tokens, completion_tokens

        additional = getattr(response_obj, "additional_kwargs", None)
        if isinstance(additional, dict):
            for key in ("usage", "token_usage"):
                prompt_tokens, completion_tokens = _extract_tokens_mapping(additional.get(key))
                if prompt_tokens is not None or completion_tokens is not None:
                    return prompt_tokens, completion_tokens
        return None, None

    def _extract_cost_from_graph(root):
        queue = deque([root])
        seen = set()
        mapping_cost_keys = (
            "response_cost",
            "cost_usd",
            "estimated_cost_usd",
            "estimated_cost",
        )
        object_cost_attrs = ("response_cost", "cost_usd")
        object_extra_attrs = (
            "_hidden_params",
            "response_metadata",
            "additional_kwargs",
            "raw",
            "raw_response",
            "model_response",
            "response",
            "original_response",
            "llm_output",
        )

        while queue:
            current = queue.popleft()
            if current is None:
                continue
            current_id = id(current)
            if current_id in seen:
                continue
            seen.add(current_id)

            if isinstance(current, dict):
                for key in mapping_cost_keys:
                    direct = _coerce_cost_usd(current.get(key))
                    if direct is not None:
                        return direct
                for value in current.values():
                    if value is not None:
                        queue.append(value)
                continue

            if isinstance(current, (list, tuple, set)):
                for value in current:
                    if value is not None:
                        queue.append(value)
                continue

            if _is_scalar(current):
                continue

            for attr in object_cost_attrs:
                direct = _coerce_cost_usd(getattr(current, attr, None))
                if direct is not None:
                    return direct

            for attr in object_extra_attrs:
                value = getattr(current, attr, None)
                if value is not None:
                    queue.append(value)

            try:
                values = vars(current).values()
            except Exception:
                values = ()
            for value in values:
                if value is not None:
                    queue.append(value)
        return None

    direct_cost = _extract_cost_from_graph(response)
    if direct_cost is not None:
        return direct_cost

    # Fallback: estimate cost from usage tokens for wrappers that hide response_cost.
    try:
        from litellm import completion_cost
    except Exception:
        return None

    prompt_tokens, completion_tokens = _extract_tokens(response)
    if prompt_tokens is None and completion_tokens is None:
        return None

    model_name = None
    response_metadata = getattr(response, "response_metadata", None)
    if isinstance(response_metadata, dict):
        model_name = (
            response_metadata.get("model_name")
            or response_metadata.get("model")
            or response_metadata.get("provider_model")
        )
    if not model_name and model is not None:
        model_name = getattr(model, "model", None) or getattr(model, "model_name", None)
    if not model_name:
        return None

    prompt_tokens = int(prompt_tokens or 0)
    completion_tokens = int(completion_tokens or 0)
    total_tokens = max(0, prompt_tokens + completion_tokens)

    try:
        # LiteLLM compatibility: recent versions expect completion_response payload.
        completion_response = {
            "model": str(model_name),
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            },
        }
        estimated = completion_cost(completion_response=completion_response)
    except TypeError:
        # Backward compatibility for older LiteLLM signatures.
        try:
            estimated = completion_cost(
                model=str(model_name),
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception:
            return None
    except Exception:
        return None
    return _coerce_cost_usd(estimated)


def _invoke_prompt_with_cost(prompt, model, parser, payload):
    messages = prompt.format_messages(**payload)
    response = model.invoke(messages)
    text = parser.invoke(response)
    return text, _extract_response_cost_usd(response, model=model)


def _invoke_doc_pass(
    model,
    parser,
    lang_meta,
    sections_format,
    chunk_text,
    chunk_evidence,
    pass_index,
    is_multi_pass,
    previous_doc,
    is_final,
    sections=None,
):
    prompt = _build_doc_prompt(
        lang_meta=lang_meta,
        sections_format=sections_format,
        pass_index=pass_index,
        is_multi_pass=is_multi_pass,
        has_previous_doc=bool(previous_doc),
        is_final=is_final,
        sections=sections,
    )
    payload = {
        "conteudo_repositorio": chunk_text,
        "evidencias": chunk_evidence,
    }
    if previous_doc:
        payload["documentacao_atual"] = previous_doc

    return _invoke_prompt_with_cost(prompt, model, parser, payload)


def _invoke_chunk_evidence_pass(
    model,
    parser,
    lang_meta,
    chunk_text,
    chunk_evidence,
    sections=None,
):
    prompt = _build_chunk_evidence_prompt(lang_meta=lang_meta, sections=sections)
    raw_output, cost_usd = _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "chunk_content": chunk_text,
            "chunk_evidence": chunk_evidence,
        },
    )
    return _parse_chunk_evidence_response(raw_output, sections=sections), cost_usd


def _invoke_functional_chunk_evidence_from_code_pass(
    model,
    parser,
    lang_meta,
    chunk_text,
    chunk_evidence,
    sections=None,
):
    prompt = _build_functional_chunk_evidence_prompt(lang_meta=lang_meta, sections=sections)
    raw_output, cost_usd = _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "chunk_content": chunk_text,
            "chunk_evidence": chunk_evidence,
        },
    )
    return _parse_chunk_evidence_response(raw_output, sections=sections), cost_usd


def _invoke_final_doc_from_evidence_pass(
    model,
    parser,
    lang_meta,
    sections_format,
    consolidated_evidence,
    global_summary,
    sections=None,
):
    prompt = _build_final_doc_from_evidence_prompt(
        lang_meta=lang_meta,
        sections_format=sections_format,
        sections=sections,
    )
    return _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "consolidated_evidence": consolidated_evidence,
            "global_summary": global_summary,
        },
    )


def _invoke_section_doc_from_context_pass(
    model,
    parser,
    lang_meta,
    section_key,
    section_context,
    global_summary,
    sections=None,
):
    prompt = _build_section_doc_from_context_prompt(
        lang_meta=lang_meta,
        section_key=section_key,
        sections=sections,
    )
    return _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "section_context": section_context,
            "global_summary": global_summary or "",
        },
    )


def _invoke_final_cleanup_pass(
    model,
    parser,
    lang_meta,
    sections_format,
    current_doc,
    supporting_evidence="",
    sections=None,
):
    prompt = _build_final_cleanup_prompt(
        lang_meta=lang_meta,
        sections_format=sections_format,
        sections=sections,
    )
    return _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "supporting_evidence": supporting_evidence or "",
            "documentacao_atual": current_doc,
        },
    )


def _build_functional_chunk_summary_prompt(lang_meta):
    from langchain_core.prompts import ChatPromptTemplate

    system_text = f"""
            You are a principal business analyst extracting functional facts from technical documentation chunks.

            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            GOAL:
            - Convert technical details into functional understanding.
            - Focus on business objectives, process behavior, rules, exceptions, operational impact, and outcomes.
            - Do not produce final sectioned documentation yet.

            RULES:
            - Use only facts explicitly present in the chunk.
            - Do not invent business context not supported by the input.
            - Avoid deep code-level details unless they are required to explain functional behavior.
            - Never mention chunking process, extraction process, evidence packs, pending markers, or workflow stages.
            - No meta-commentary about what is missing in the chunk.
            - Keep output concise but detailed enough for downstream section writing.
            - Prefer compact paragraphs and focused bullets.

            OUTPUT:
            - Return plain markdown text only (no JSON).
            - Start with a short paragraph summarizing what this chunk contributes functionally.
            - Then include concise bullets grouped by functional signal when useful.
            """
    user_text = "TECHNICAL DOCUMENTATION CHUNK:\n{chunk_text}"
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_functional_section_doc_from_context_prompt(lang_meta, section_key, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    sections_map = _active_sections(
        sections,
        default_sections=FUNCTIONAL_DOCUMENTATION_SECTIONS,
    )
    section = sections_map.get(section_key)
    if section is None:
        raise ValueError(f"Unknown functional documentation section key: {section_key}")

    section_style_target = _escape_prompt_literal(
        _section_style_target_line(
            section_key,
            sections=sections_map,
            style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
        )
    )
    required_format = (
        f"<!-- SECTION:{section_key} -->\n"
        f"# {section['title']}\n"
        "(Write only this section content)\n"
    )
    required_format_escaped = _escape_prompt_literal(required_format)
    section_title_escaped = _escape_prompt_literal(section["title"])

    system_text = f"""
            You are a principal business analyst writing one functional documentation section.

            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            OBJECTIVE:
            - Write only the requested section with strong functional detail.
            - Prioritize process, rules, exceptions, stakeholder actions, operational routines, and outcomes.
            - Do not focus on implementation internals unless strictly needed for functional understanding.

            RULES:
            - Output exactly one section: {section_key} ({section_title_escaped}).
            - Do not output any other section marker or title.
            - Do not mention chunking, extraction, evidence packs, pending markers, or workflow stages.
            - Do not include labels like "Observação", "Nota", "Observação de evidência", or "Limitações de evidência".
            - Do not add custom AI-generation disclaimers.
            - Use impersonal professional tone; avoid second-person address.
            - Do not invent facts.
            - If information is insufficient, state the limitation directly and cleanly inside the section.

            SECTION STYLE TARGET:
            - {section_style_target}

            Required output format:
            {required_format_escaped}
            """
    user_text = "FUNCTIONAL CONTEXT:\n{section_context}"
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _build_functional_final_cleanup_prompt(lang_meta, sections_format, sections=None):
    from langchain_core.prompts import ChatPromptTemplate

    section_style_guide = _escape_prompt_literal(
        _build_section_style_guide(
            sections=sections,
            style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
        )
    )
    marker_examples = _escape_prompt_literal(", ".join(INTERMEDIATE_MARKERS))
    sections_format_escaped = _escape_prompt_literal(sections_format)
    system_text = f"""
            You are a senior business analyst finalizing functional documentation.

            Target language: {lang_meta['name']}.
            {lang_meta['strict_rule']}

            Your task: rewrite the full functional documentation into a coherent final version.

            FINALIZATION RULES:
            - You have editorial freedom to improve fluency, coherence, and organization.
            - You may reorder, merge, or split paragraphs and bullets inside each section.
            - Preserve all section delimiters and exact section titles from the required format.
            - Keep every required section present exactly once and non-empty.
            - Remove temporary workflow markers and stage labels, including: {marker_examples}.
            - Remove references to chunking, extraction process, pending content, and "new evidence".
            - Remove commentary labels such as "Observação", "Nota", "Observação de evidência", "Limitações de evidência".
            - Remove meta-writing mentions of evidence; present functional facts directly.
            - Use impersonal professional tone; avoid second-person instructions.
            - Remove custom AI-generation disclaimers; a standard disclaimer is injected automatically.
            - FACT FIDELITY IS MANDATORY: do not add new facts, entities, rules, constraints, paths, commands, metrics, or claims.
            - Only reorganize and rephrase information already present in DOCUMENTACAO_ATUAL.
            - If unsure about a detail, remove it instead of inventing.

            SECTION STYLE TARGETS:
            {section_style_guide}

            Required output format:

            {sections_format_escaped}
            """
    user_text = (
        "SOURCE FUNCTIONAL CONTEXT:\n{supporting_context}\n\n"
        "DOCUMENTACAO_ATUAL:\n{documentacao_atual}"
    )
    return ChatPromptTemplate.from_messages([("system", system_text), ("user", user_text)])


def _invoke_functional_chunk_summary_pass(
    model,
    parser,
    lang_meta,
    chunk_text,
):
    prompt = _build_functional_chunk_summary_prompt(lang_meta=lang_meta)
    return _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "chunk_text": chunk_text,
        },
    )


def _invoke_functional_section_doc_from_context_pass(
    model,
    parser,
    lang_meta,
    section_key,
    section_context,
    sections=None,
):
    prompt = _build_functional_section_doc_from_context_prompt(
        lang_meta=lang_meta,
        section_key=section_key,
        sections=sections,
    )
    return _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "section_context": section_context,
        },
    )


def _invoke_functional_final_cleanup_pass(
    model,
    parser,
    lang_meta,
    sections_format,
    current_doc,
    supporting_context="",
    sections=None,
):
    prompt = _build_functional_final_cleanup_prompt(
        lang_meta=lang_meta,
        sections_format=sections_format,
        sections=sections,
    )
    return _invoke_prompt_with_cost(
        prompt,
        model,
        parser,
        {
            "supporting_context": supporting_context or "",
            "documentacao_atual": current_doc,
        },
    )


def _compress_text_blocks_to_budget(blocks, budget_tokens):
    import re

    clean_blocks = [str(block or "").strip() for block in (blocks or []) if str(block or "").strip()]
    if not clean_blocks:
        return ""

    budget_tokens = max(1, int(budget_tokens))
    char_budget = max(256, budget_tokens * 4)
    merged = "\n\n".join(clean_blocks)
    if len(merged) <= char_budget:
        return merged

    per_block = max(160, int(char_budget / max(1, len(clean_blocks))) - 2)
    clipped = []
    for block in clean_blocks:
        if len(block) <= per_block:
            clipped.append(block)
            continue
        snippet = block[:per_block].strip()
        snippet = re.sub(r"\s+\S*$", "", snippet).strip()
        clipped.append(snippet if snippet else block[:per_block].strip())
    merged = "\n\n".join(clipped)
    if len(merged) <= char_budget:
        return merged
    return merged[:char_budget].strip()


def _expand_inline_pseudo_lists(text):
    import re

    if not text:
        return text

    normalized_lines = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        stripped = line.strip()
        if not stripped:
            normalized_lines.append(raw_line)
            continue

        if (
            stripped.startswith("#")
            or stripped.startswith("- ")
            or stripped.startswith("* ")
            or stripped.startswith("```")
            or " - " not in stripped
        ):
            normalized_lines.append(raw_line)
            continue

        if stripped.count(" - ") < 2:
            normalized_lines.append(raw_line)
            continue

        parts = [part.strip() for part in re.split(r"\s+-\s+", stripped) if part.strip()]
        if len(parts) < 3:
            normalized_lines.append(raw_line)
            continue

        lead = parts[0]
        items = parts[1:]
        if len(lead.split()) > 18 or any(len(item) < 5 for item in items):
            normalized_lines.append(raw_line)
            continue

        indent = raw_line[: len(raw_line) - len(raw_line.lstrip())]
        heading = lead if lead.endswith(":") else f"{lead}:"
        normalized_lines.append(f"{indent}{heading}")
        for item in items:
            normalized_lines.append(f"{indent}- {item}")

    return "\n".join(normalized_lines)


def _normalize_ordered_list_markers(text):
    import re

    if not text:
        return text

    out = []
    in_fence = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(raw_line)
            continue
        if in_fence:
            out.append(raw_line)
            continue

        # Normalize "1) item" -> "1. item" for markdown compatibility.
        line = re.sub(r"^(\s*)(\d+)\)\s+", r"\1\2. ", raw_line)
        out.append(line)
    return "\n".join(out)


def _promote_bullet_headings_with_children(text):
    import re

    if not text:
        return text

    lines = text.splitlines()
    out = []
    i = 0

    def _line_indent(value):
        return len(value) - len(value.lstrip(" "))

    def _is_child_marker(value):
        stripped = value.lstrip()
        return (
            stripped.startswith("- ")
            or stripped.startswith("* ")
            or bool(re.match(r"^\d+\.\s+", stripped))
        )

    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        indent = _line_indent(line)

        if not stripped.startswith("- "):
            out.append(line)
            i += 1
            continue

        content = stripped[2:].strip()
        if not content:
            out.append(line)
            i += 1
            continue

        # Find next non-empty line to check if this bullet behaves as a heading.
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1

        if j >= len(lines):
            out.append(line)
            i += 1
            continue

        next_line = lines[j]
        next_indent = _line_indent(next_line)
        next_is_child = _is_child_marker(next_line)
        if next_is_child and next_indent > indent:
            heading = content.rstrip()
            if not heading.endswith(":"):
                heading += ":"
            out.append((" " * indent) + heading)
            i += 1
            continue

        out.append(line)
        i += 1

    return "\n".join(out)


def _collapse_short_explanatory_bullets(text):
    import re

    if not text:
        return text

    lines = text.splitlines()
    out = []
    i = 0

    def _is_bullet(line):
        return line.lstrip().startswith("- ")

    def _bullet_content(line):
        stripped = line.lstrip()
        return stripped[2:].strip()

    def _normalize_sentence(value):
        sentence = value.strip()
        if sentence and not re.search(r"[.!?]$", sentence):
            sentence += "."
        return sentence

    while i < len(lines):
        line = lines[i]
        if not _is_bullet(line):
            out.append(line)
            i += 1
            continue

        start = i
        block = []
        while i < len(lines) and _is_bullet(lines[i]):
            block.append(lines[i])
            i += 1

        # Keep structured lists; collapse only short explanatory blocks.
        if len(block) > 2:
            out.extend(block)
            continue

        contents = [_bullet_content(item) for item in block]
        if not contents or any(len(c) < 50 for c in contents):
            out.extend(block)
            continue
        if any("`" in c for c in contents):
            out.extend(block)
            continue
        if any(c.endswith(":") for c in contents):
            out.extend(block)
            continue

        prev_non_empty = ""
        for j in range(len(out) - 1, -1, -1):
            candidate = out[j].strip()
            if candidate:
                prev_non_empty = candidate
                break
        if prev_non_empty.endswith(":"):
            out.extend(block)
            continue

        indent = block[0][: len(block[0]) - len(block[0].lstrip())]
        paragraph = " ".join(_normalize_sentence(c) for c in contents if c)
        if not paragraph:
            out.extend(block)
            continue
        out.append(f"{indent}{paragraph}")

    return "\n".join(out)


def _rebalance_excess_bullets_by_section(text, style_rules=None):
    import re

    if not text:
        return text

    active_rules = (
        style_rules
        if isinstance(style_rules, dict) and style_rules
        else SECTION_STYLE_RULES
    )

    marker_re = re.compile(r"^\s*<!--\s*SECTION:([A-Z_]+)\s*-->\s*$")

    def _is_bullet(line):
        return line.lstrip().startswith("- ")

    def _bullet_content(line):
        return line.lstrip()[2:].strip()

    def _normalize_sentence(value):
        sentence = value.strip()
        if sentence and not re.search(r"[.!?]$", sentence):
            sentence += "."
        return sentence

    def _is_command_like(content):
        value = content.lower()
        if "`" in content:
            return True
        if re.search(r"\b(python|pip|poetry|pytest|tox|make|uv|npm|yarn|cargo)\b", value):
            return True
        if re.search(r"\b\.ya?ml\b|\b\.toml\b|\b\.json\b|\b\.ini\b", value):
            return True
        return False

    def _flush_paragraph_buffer(out_lines, buffer_items):
        if not buffer_items:
            return
        group_size = 2
        idx = 0
        while idx < len(buffer_items):
            group = buffer_items[idx : idx + group_size]
            paragraph = " ".join(_normalize_sentence(item) for item in group if item.strip())
            if paragraph:
                out_lines.append(paragraph)
            idx += group_size

    def _rebalance_section_lines(section_key, section_lines):
        rules = active_rules.get(section_key, {})
        max_bullets_raw = rules.get("max_bullets", 8)
        if max_bullets_raw is None:
            return section_lines
        max_bullets = max(0, int(max_bullets_raw))

        bullet_positions = [idx for idx, ln in enumerate(section_lines) if _is_bullet(ln)]
        if len(bullet_positions) <= max_bullets:
            return section_lines

        overflow = len(bullet_positions) - max_bullets

        preferred_remove = []
        fallback_remove = []
        for pos in bullet_positions[max_bullets:]:
            content = _bullet_content(section_lines[pos])
            if not content:
                fallback_remove.append(pos)
                continue
            if len(content) >= 45 and not _is_command_like(content):
                preferred_remove.append(pos)
            else:
                fallback_remove.append(pos)

        remove_positions = preferred_remove[:overflow]
        if len(remove_positions) < overflow:
            need = overflow - len(remove_positions)
            remove_positions.extend(fallback_remove[:need])
        remove_set = set(remove_positions)

        out = []
        paragraph_buffer = []
        for idx, ln in enumerate(section_lines):
            if idx in remove_set and _is_bullet(ln):
                paragraph_buffer.append(_bullet_content(ln))
                continue
            if paragraph_buffer:
                _flush_paragraph_buffer(out, paragraph_buffer)
                paragraph_buffer = []
            out.append(ln)

        if paragraph_buffer:
            _flush_paragraph_buffer(out, paragraph_buffer)

        return out

    lines = text.splitlines()
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        marker_match = marker_re.match(line.strip())
        if not marker_match:
            out_lines.append(line)
            i += 1
            continue

        section_key = marker_match.group(1).strip()
        out_lines.append(line)
        i += 1
        section_start = i
        while i < len(lines) and not marker_re.match(lines[i].strip()):
            i += 1
        section_chunk = lines[section_start:i]
        out_lines.extend(_rebalance_section_lines(section_key, section_chunk))

    return "\n".join(out_lines)


def _standard_ai_disclaimer(language):
    lang = _normalize_doc_language(language)
    return STANDARD_AI_DISCLAIMER_BY_LANG.get(lang, STANDARD_AI_DISCLAIMER_BY_LANG["EN-US"])


def _is_ai_disclaimer_variant_line(text):
    import re

    value = str(text or "").strip().lower()
    if not value:
        return False
    normalized = re.sub(r"[*_`]+", "", value)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    alnum_only = re.sub(r"[^0-9a-z\u00c0-\u024f]+", " ", normalized, flags=re.IGNORECASE)
    alnum_only = re.sub(r"\s+", " ", alnum_only).strip()

    for candidate in (value, normalized, alnum_only):
        if not candidate:
            continue
        for pattern in AI_DISCLAIMER_VARIANT_PATTERNS:
            if re.search(pattern, candidate, flags=re.IGNORECASE):
                return True

    tokens = set(alnum_only.split())
    has_notice_word = any(word in tokens for word in {"aviso", "notice", "avis", "hinweis"})
    has_ai_word = any(word in tokens for word in {"ia", "ai", "ki"})
    has_generated_word = any(
        frag in alnum_only
        for frag in (
            "gerado",
            "gerada",
            "generated",
            "generado",
            "generada",
            "genere",
            "generee",
            "erzeugt",
            "erstellt",
            "automatic",
            "automatica",
            "automaticamente",
        )
    )
    if has_notice_word and has_ai_word and has_generated_word:
        return True
    return False


def _strip_ai_disclaimer_variants(text):
    if not text:
        return text

    lines = text.splitlines()
    filtered = []
    i = 0
    while i < len(lines):
        current = lines[i]
        stripped = current.strip()

        # Remove full blockquote disclaimer paragraphs (including multiline).
        if stripped.startswith(">"):
            quote_block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_block.append(lines[i])
                i += 1
            quote_text = " ".join(
                part.strip().lstrip(">").strip() for part in quote_block if part.strip()
            )
            if _is_ai_disclaimer_variant_line(quote_text):
                while i < len(lines) and not lines[i].strip():
                    i += 1
                continue
            filtered.extend(quote_block)
            continue

        if _is_ai_disclaimer_variant_line(current):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue
        filtered.append(current)
        i += 1
    return "\n".join(filtered)


def _inject_standard_ai_disclaimer(text, language):
    doc = _strip_ai_disclaimer_variants(text or "")
    disclaimer = _standard_ai_disclaimer(language)
    if not disclaimer:
        return doc

    lines = doc.splitlines()
    section_marker = "<!-- SECTION:INDEX -->"
    marker_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == section_marker:
            marker_idx = i
            break

    if marker_idx == -1:
        for i, line in enumerate(lines):
            if line.strip().startswith("<!-- SECTION:"):
                marker_idx = i
                break
        if marker_idx == -1:
            prefix = [disclaimer, ""]
            return "\n".join(prefix + lines).strip() + "\n"

    next_section_idx = len(lines)
    for i in range(marker_idx + 1, len(lines)):
        if lines[i].strip().startswith("<!-- SECTION:"):
            next_section_idx = i
            break

    heading_idx = -1
    for i in range(marker_idx + 1, next_section_idx):
        if lines[i].lstrip().startswith("# "):
            heading_idx = i
            break

    if heading_idx == -1:
        insert_at = marker_idx + 1
    else:
        insert_at = heading_idx + 1
        while insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1

    updated = []
    updated.extend(lines[:insert_at])
    if updated and updated[-1].strip():
        updated.append("")
    updated.append(disclaimer)
    updated.append("")
    updated.extend(lines[insert_at:])
    return "\n".join(updated).strip() + "\n"


def apply_standard_ai_disclaimer(text, language):
    return _inject_standard_ai_disclaimer(text, language)


def _number_document_headings(text):
    import re

    if not text:
        return text

    lines = str(text).splitlines()
    out = []
    in_fence = False
    counters = [0] * 7  # 1..6

    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(raw_line)
            continue
        if in_fence:
            out.append(raw_line)
            continue

        match = re.match(r"^(\s*)(#{1,6})\s+(.+?)\s*$", raw_line)
        if not match:
            out.append(raw_line)
            continue

        indent, hashes, title = match.group(1), match.group(2), match.group(3).strip()
        level = len(hashes)
        # Idempotent numbering: remove existing heading numbering before reapplying.
        title = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", title).strip()

        counters[level] += 1
        for idx in range(level + 1, 7):
            counters[idx] = 0
        for idx in range(1, level):
            if counters[idx] == 0:
                counters[idx] = 1

        if level == 1:
            number = f"{counters[1]}."
        else:
            number = ".".join(str(counters[idx]) for idx in range(1, level + 1))
        out.append(f"{indent}{hashes} {number} {title}".rstrip())

    return "\n".join(out)


def _strip_intermediate_markers(text, normalize_structure=True, style_rules=None):
    import re

    if not text:
        return text

    marker_pattern = re.compile(
        r"\[(?:\s*pending\s*|\s*pendente\s*|\s*evid[eê]ncia\s+nova\s*|\s*new\s+evidence\s*)\]",
        flags=re.IGNORECASE,
    )
    text = marker_pattern.sub("", text)

    phrase_patterns = [
        r"\bevid[eê]ncia\s+nova\b:?\s*",
        r"\bnew\s+evidence\b:?\s*",
        r"\bpendente\b:?\s*",
        r"\bpending\b:?\s*",
        r"\bnovo\s+trecho\s+do\s+repositorio\b:?\s*",
    ]
    for pat in phrase_patterns:
        text = re.sub(pat, "", text, flags=re.IGNORECASE)

    text = re.sub(r"\(\s*veja abaixo\s*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bveja abaixo\b", "", text, flags=re.IGNORECASE)

    lines = text.splitlines()
    deduped_lines = []
    seen_bullets = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            key = _canonical_evidence_key(stripped)
            if key in seen_bullets:
                continue
            seen_bullets.add(key)
        if _is_meta_process_statement(stripped):
            continue
        if _is_doc_meta_line(stripped):
            continue
        deduped_lines.append(line)
    text = "\n".join(deduped_lines)
    if normalize_structure:
        text = _expand_inline_pseudo_lists(text)
        text = _normalize_ordered_list_markers(text)
        text = _promote_bullet_headings_with_children(text)
        text = _collapse_short_explanatory_bullets(text)
        text = _rebalance_excess_bullets_by_section(text, style_rules=style_rules)

    text = _number_document_headings(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def generate_doc(
    input_json,
    output_md='documentacao.md',
    language='PT-BR',
    provider='gemini',
    model_name='gemini-2.5-flash',
    api_key=None,
    use_system_key=True,
    context_window_tokens=DEFAULT_CONTEXT_WINDOW_TOKENS,
    prompt_overhead_tokens=DEFAULT_PROMPT_OVERHEAD_TOKENS,
    output_reserve_tokens=DEFAULT_OUTPUT_RESERVE_TOKENS,
    min_chunk_tokens=DEFAULT_MIN_CHUNK_TOKENS,
    hard_total_token_limit=DEFAULT_MAX_TOTAL_TOKENS,
    max_llm_calls=DEFAULT_MAX_LLM_CALLS,
    request_token_cap=None,
    tpm_limit_tokens=None,
    progress_callback=None,
    documentation_sections=None,
    resume_from_checkpoint=False,
    checkpoint_path=None,
    documentation_kind="technical",
):
    import json
    import time
    from pathlib import Path
    from langchain_core.output_parsers import StrOutputParser
    from src.llm_utils import init_llm

    doc_kind = str(documentation_kind or "technical").strip().lower()
    if doc_kind not in {"technical", "functional"}:
        raise ValueError("documentation_kind must be 'technical' or 'functional'.")
    is_functional_doc = doc_kind == "functional"
    default_sections_map = (
        FUNCTIONAL_DOCUMENTATION_SECTIONS if is_functional_doc else DOCUMENTATION_SECTIONS
    )
    cleanup_style_rules = FUNCTIONAL_SECTION_STYLE_RULES if is_functional_doc else None
    log_prefix_tag = "functional_doc_gen" if is_functional_doc else "doc_gen"

    def _log(message):
        print(f"[{log_prefix_tag}] {message}", flush=True)

    def _emit_progress(event, **payload):
        if progress_callback is None:
            return
        data = {"event": event}
        data.update(payload)
        try:
            progress_callback(data)
        except Exception:
            pass

    context_window_tokens = int(context_window_tokens)
    prompt_overhead_tokens = int(prompt_overhead_tokens)
    output_reserve_tokens = int(output_reserve_tokens)
    min_chunk_tokens = int(min_chunk_tokens)
    hard_total_token_limit = int(hard_total_token_limit)
    max_llm_calls = int(max_llm_calls)
    resolved_request_token_cap = _resolve_request_token_cap(provider, model_name, request_token_cap)
    resolved_tpm_limit = _resolve_tpm_limit(provider, model_name, tpm_limit_tokens)

    if context_window_tokens <= 0:
        raise ValueError("context_window_tokens must be positive.")
    if hard_total_token_limit <= 0:
        raise ValueError("hard_total_token_limit must be positive.")
    if max_llm_calls <= 0:
        raise ValueError("max_llm_calls must be positive.")

    effective_request_limit = context_window_tokens
    if resolved_request_token_cap is not None:
        effective_request_limit = min(effective_request_limit, resolved_request_token_cap)

    single_pass_budget = effective_request_limit - prompt_overhead_tokens - output_reserve_tokens
    if single_pass_budget <= 0:
        raise ValueError(
            "Invalid token budget configuration. Increase context window or reduce prompt/output reserves."
        )

    with open(input_json, 'r', encoding='utf-8') as repositorio:
        lista_repositorio = json.load(repositorio)

    files_for_doc = _collect_file_payloads(lista_repositorio)
    files_for_doc = _sort_files_for_doc(files_for_doc)

    if not files_for_doc:
        raise ValueError(
            "Nenhum arquivo analisável encontrado (todos foram ignorados). "
            "Verifique os filtros de arquivos e gere o code.json novamente."
        )

    tokens_total = sum(max(1, int(item.get("tokens", 0) or 1)) for item in files_for_doc)
    if tokens_total > hard_total_token_limit:
        raise ValueError(
            f"Repositório grande demais para processar com segurança: {tokens_total} tokens estimados "
            f"(limite: {hard_total_token_limit})."
        )

    model = init_llm(
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        use_system_key=use_system_key,
        temperature=0,
    )

    parser = StrOutputParser()
    lang_meta = _language_meta(language)
    runtime_sections = _coerce_runtime_sections(
        documentation_sections,
        default_sections=default_sections_map,
    )
    sections_format = _build_sections_format(sections=runtime_sections)
    section_keys = list(runtime_sections.keys())
    section_count = len(section_keys)
    checkpoint_file = (
        Path(checkpoint_path)
        if checkpoint_path
        else (
            Path(input_json).resolve().parent
            / ("functional_code_doc_gen_resume.json" if is_functional_doc else "doc_gen_resume.json")
        )
    )

    def _resume_signature():
        return {
            "version": 1,
            "input_json": str(Path(input_json).resolve()),
            "input_mtime": float(Path(input_json).stat().st_mtime),
            "language": str(language or ""),
            "provider": str(provider or ""),
            "model_name": str(model_name or ""),
            "documentation_kind": str(doc_kind),
            "context_window_tokens": int(context_window_tokens),
            "prompt_overhead_tokens": int(prompt_overhead_tokens),
            "output_reserve_tokens": int(output_reserve_tokens),
            "min_chunk_tokens": int(min_chunk_tokens),
            "hard_total_token_limit": int(hard_total_token_limit),
            "max_llm_calls": int(max_llm_calls),
            "request_token_cap": (
                int(resolved_request_token_cap)
                if resolved_request_token_cap is not None
                else None
            ),
            "tpm_limit_tokens": (
                int(resolved_tpm_limit) if resolved_tpm_limit is not None else None
            ),
            "sections": runtime_sections,
        }

    def _save_checkpoint_state(state):
        payload = {
            "version": 1,
            "signature": _resume_signature(),
            "state": state,
            "saved_at": time.time(),
        }
        checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_file.write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )

    def _clear_checkpoint_state():
        try:
            if checkpoint_file.exists():
                checkpoint_file.unlink()
        except Exception:
            pass

    def _load_checkpoint_state():
        if not resume_from_checkpoint:
            return None
        try:
            if not checkpoint_file.exists():
                return None
            payload = json.loads(checkpoint_file.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return None
            if payload.get("signature") != _resume_signature():
                return None
            state = payload.get("state")
            if isinstance(state, dict):
                return state
        except Exception:
            return None
        return None

    llm_calls = 0
    estimated_processing_tokens = 0
    tpm_events = []
    is_multi_pass = tokens_total > single_pass_budget
    total_calls_hint = 1
    total_cost_usd = 0.0
    cost_samples = 0
    resume_state = _load_checkpoint_state()
    resume_phase = str(resume_state.get("phase") or "") if isinstance(resume_state, dict) else ""

    if resume_state:
        try:
            llm_calls = max(0, int(resume_state.get("llm_calls", llm_calls)))
        except Exception:
            llm_calls = 0
        try:
            estimated_processing_tokens = max(
                0,
                int(resume_state.get("estimated_processing_tokens", estimated_processing_tokens)),
            )
        except Exception:
            estimated_processing_tokens = 0
        try:
            total_calls_hint = max(
                total_calls_hint,
                int(resume_state.get("total_calls_hint", total_calls_hint)),
            )
        except Exception:
            pass
        try:
            total_cost_usd = max(0.0, float(resume_state.get("total_cost_usd", total_cost_usd)))
        except Exception:
            total_cost_usd = 0.0
        try:
            cost_samples = max(0, int(resume_state.get("cost_samples", cost_samples)))
        except Exception:
            cost_samples = 0
        _log(
            "resume-state "
            f"phase={resume_phase or 'none'} "
            f"llm_calls={llm_calls} "
            f"estimated_processing_tokens={estimated_processing_tokens} "
            f"total_cost_usd={total_cost_usd:.6f}"
        )
    else:
        # Fresh run starts from a clean checkpoint file.
        _clear_checkpoint_state()
    total_calls_hint = max(total_calls_hint, llm_calls + 1)

    def _save_resume_phase(phase, **extra):
        state = {
            "phase": str(phase or ""),
            "llm_calls": int(llm_calls),
            "estimated_processing_tokens": int(estimated_processing_tokens),
            "total_calls_hint": int(total_calls_hint),
            "total_cost_usd": float(total_cost_usd),
            "cost_samples": int(cost_samples),
        }
        state.update(extra)
        _save_checkpoint_state(state)

    _log(
        "start "
        f"files={len(files_for_doc)} "
        f"tokens_total={tokens_total} "
        f"provider={provider} "
        f"model={model_name} "
        f"effective_request_limit={effective_request_limit} "
        f"tpm_limit={resolved_tpm_limit if resolved_tpm_limit is not None else 'none'}"
    )

    if is_multi_pass:
        initial_chunk_budget = effective_request_limit - prompt_overhead_tokens - output_reserve_tokens
        estimated_calls = _estimate_initial_multi_pass_calls(
            files=files_for_doc,
            token_budget=initial_chunk_budget,
            min_chunk_tokens=min_chunk_tokens,
            max_llm_calls=max_llm_calls,
        )
        # Reserve extraction + one writing call per section + cleanup.
        total_calls_hint = max(
            total_calls_hint,
            section_count + 2,
            estimated_calls + section_count + 2,
        )
        _emit_progress(
            "plan",
            is_multi_pass=True,
            total_calls=total_calls_hint,
            message="Large repository detected. Documentation generation may take a few minutes.",
            total_cost_usd=total_cost_usd,
            cost_available=False,
        )
    else:
        total_calls_hint = max(total_calls_hint, 1, section_count + 1)
        _emit_progress(
            "plan",
            is_multi_pass=False,
            total_calls=total_calls_hint,
            message="",
            total_cost_usd=total_cost_usd,
            cost_available=False,
        )

    def _reserve_tpm_capacity(estimated_call_tokens):
        if resolved_tpm_limit is None:
            return
        if estimated_call_tokens > resolved_tpm_limit:
            raise ValueError(
                "Estimated request size exceeds configured TPM cap for a single call. "
                f"Estimated={int(estimated_call_tokens)}, tpm_cap={int(resolved_tpm_limit)}."
            )

        while True:
            now = time.monotonic()
            tpm_events[:] = [(ts, tok) for ts, tok in tpm_events if (now - ts) < 60.0]
            used = sum(tok for _, tok in tpm_events)
            if used + estimated_call_tokens <= resolved_tpm_limit:
                tpm_events.append((now, int(estimated_call_tokens)))
                return
            oldest_ts = tpm_events[0][0] if tpm_events else now
            sleep_for = max(0.05, 60.0 - (now - oldest_ts) + 0.05)
            _log(
                "tpm-wait "
                f"used_last_min={used} "
                f"next_call_tokens={int(estimated_call_tokens)} "
                f"limit={resolved_tpm_limit} "
                f"sleep_s={sleep_for:.2f}"
            )
            time.sleep(sleep_for)

    def _ensure_call_limits(estimated_call_tokens):
        nonlocal llm_calls, estimated_processing_tokens
        if estimated_call_tokens > effective_request_limit:
            raise ValueError(
                "Estimated request size exceeds configured per-call token limit. "
                f"Estimated={int(estimated_call_tokens)}, limit={int(effective_request_limit)}."
            )
        _reserve_tpm_capacity(estimated_call_tokens)
        llm_calls += 1
        if llm_calls > max_llm_calls:
            raise ValueError(
                f"Aborted for safety: number of LLM calls exceeded limit ({max_llm_calls})."
            )
        estimated_processing_tokens += max(0, int(estimated_call_tokens))
        if estimated_processing_tokens > hard_total_token_limit:
            raise ValueError(
                f"Aborted for safety: cumulative processing estimate exceeded {hard_total_token_limit} tokens."
            )

    def _register_call_cost(call_cost):
        nonlocal total_cost_usd, cost_samples
        value = _coerce_cost_usd(call_cost)
        if value is None:
            return None
        total_cost_usd += value
        cost_samples += 1
        return value

    def _invoke_chunk_extraction_pass(chunk_text, chunk_evidence):
        if is_functional_doc:
            return _invoke_functional_chunk_evidence_from_code_pass(
                model=model,
                parser=parser,
                lang_meta=lang_meta,
                sections=runtime_sections,
                chunk_text=chunk_text,
                chunk_evidence=chunk_evidence,
            )
        return _invoke_chunk_evidence_pass(
            model=model,
            parser=parser,
            lang_meta=lang_meta,
            sections=runtime_sections,
            chunk_text=chunk_text,
            chunk_evidence=chunk_evidence,
        )

    def _invoke_section_writer_pass(section_key, section_context, global_summary_text):
        if is_functional_doc:
            return _invoke_functional_section_doc_from_context_pass(
                model=model,
                parser=parser,
                lang_meta=lang_meta,
                section_key=section_key,
                sections=runtime_sections,
                section_context=section_context,
            )
        return _invoke_section_doc_from_context_pass(
            model=model,
            parser=parser,
            lang_meta=lang_meta,
            section_key=section_key,
            sections=runtime_sections,
            section_context=section_context,
            global_summary=global_summary_text,
        )

    def _invoke_cleanup_pass(current_doc_text, supporting_text):
        if is_functional_doc:
            return _invoke_functional_final_cleanup_pass(
                model=model,
                parser=parser,
                lang_meta=lang_meta,
                sections_format=sections_format,
                sections=runtime_sections,
                current_doc=current_doc_text,
                supporting_context=supporting_text,
            )
        return _invoke_final_cleanup_pass(
            model=model,
            parser=parser,
            lang_meta=lang_meta,
            sections_format=sections_format,
            sections=runtime_sections,
            current_doc=current_doc_text,
            supporting_evidence=supporting_text,
        )

    def _strip_doc_markers(text, *, normalize_structure):
        if cleanup_style_rules is None:
            return _strip_intermediate_markers(
                text,
                normalize_structure=normalize_structure,
            )
        return _strip_intermediate_markers(
            text,
            normalize_structure=normalize_structure,
            style_rules=cleanup_style_rules,
        )

    def _write_sections_from_context(
        section_context,
        context_tokens,
        supporting_summary,
        *,
        is_multi_phase,
        phase_name,
        log_prefix,
        initial_section_outputs=None,
        start_section_index=1,
        checkpoint_phase=None,
        checkpoint_extra=None,
    ):
        nonlocal total_calls_hint

        section_outputs = dict(initial_section_outputs or {})
        context_tokens = max(0, int(context_tokens))
        summary_for_call = supporting_summary or ""
        summary_tokens = _approx_tokens_text(summary_for_call)
        if (
            prompt_overhead_tokens + output_reserve_tokens + context_tokens + summary_tokens
            > effective_request_limit
            and summary_tokens > 0
        ):
            summary_for_call = ""
            summary_tokens = 0
        total_sections = len(section_keys)

        try:
            start_idx = int(start_section_index)
        except Exception:
            start_idx = 1
        start_idx = max(1, min(start_idx, len(section_keys) + 1))

        for section_idx in range(start_idx, len(section_keys) + 1):
            section_key = section_keys[section_idx - 1]
            current_call = llm_calls + 1
            remaining_section_calls = total_sections - section_idx
            total_calls_hint = max(total_calls_hint, current_call + remaining_section_calls + 1)

            estimated_call = (
                prompt_overhead_tokens
                + output_reserve_tokens
                + context_tokens
                + summary_tokens
            )
            _log(
                f"{log_prefix} section={section_key} "
                f"index={section_idx}/{total_sections} "
                f"context_tokens={context_tokens} "
                f"summary_tokens={summary_tokens} "
                f"estimated_call={estimated_call}"
            )
            _emit_progress(
                "call_start",
                is_multi_pass=is_multi_phase,
                current_call=current_call,
                total_calls=total_calls_hint,
                phase=phase_name,
            )
            _ensure_call_limits(estimated_call)
            section_text, call_cost_usd = _invoke_section_writer_pass(
                section_key=section_key,
                section_context=section_context,
                global_summary_text=summary_for_call,
            )
            section_outputs[section_key] = section_text
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=is_multi_phase,
                current_call=llm_calls,
                total_calls=total_calls_hint,
                phase=phase_name,
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            if checkpoint_phase:
                extra_payload = {}
                if callable(checkpoint_extra):
                    try:
                        extra_payload = checkpoint_extra(dict(section_outputs), section_idx + 1) or {}
                    except Exception:
                        extra_payload = {}
                _save_resume_phase(
                    checkpoint_phase,
                    section_outputs=section_outputs,
                    next_section_index=min(len(section_keys) + 1, section_idx + 1),
                    **extra_payload,
                )

        return (
            _assemble_document_from_sections(
                section_outputs,
                language=language,
                sections=runtime_sections,
            ),
            section_outputs,
        )

    global_summary = _build_repo_evidence_snapshot(files_for_doc)
    refinement_done_by_llm = False

    if tokens_total <= single_pass_budget:
        _log(
            f"single-pass budget={single_pass_budget} "
            f"estimated_call={prompt_overhead_tokens + output_reserve_tokens + tokens_total}"
        )
        codigo_completo = _render_repo_content(files_for_doc)
        repo_context_tokens = _approx_tokens_text(codigo_completo)
        single_outputs_seed = {}
        single_start_index = 1
        documentacao = ""
        single_cleanup_already_done = False
        if isinstance(resume_state, dict) and resume_phase == "single_section_writing":
            seed = resume_state.get("section_outputs")
            if isinstance(seed, dict):
                single_outputs_seed = dict(seed)
            try:
                single_start_index = int(resume_state.get("next_section_index") or 1)
            except Exception:
                single_start_index = 1
        elif isinstance(resume_state, dict) and resume_phase in {"single_cleanup_ready", "single_cleanup_done"}:
            resumed_doc = resume_state.get("current_doc")
            if isinstance(resumed_doc, str) and resumed_doc.strip():
                documentacao = resumed_doc
                single_cleanup_already_done = resume_phase == "single_cleanup_done"
                _log(
                    "resume single "
                    f"phase={resume_phase} "
                    f"doc_tokens={_approx_tokens_text(documentacao)}"
                )

        if not documentacao:
            documentacao, _ = _write_sections_from_context(
                section_context=codigo_completo,
                context_tokens=repo_context_tokens,
                supporting_summary=global_summary,
                is_multi_phase=False,
                phase_name="generation",
                log_prefix="single-pass section-writing",
                initial_section_outputs=single_outputs_seed,
                start_section_index=single_start_index,
                checkpoint_phase="single_section_writing",
                checkpoint_extra=lambda _outputs, _next_idx: {},
            )
            _save_resume_phase("single_cleanup_ready", current_doc=documentacao)

        single_pass_cleanup_done = False
        cleanup_supporting_evidence = global_summary
        cleanup_estimated_call = (
            prompt_overhead_tokens
            + output_reserve_tokens
            + _approx_tokens_text(cleanup_supporting_evidence)
            + _approx_tokens_text(documentacao)
        )
        if single_cleanup_already_done:
            single_pass_cleanup_done = True
        elif cleanup_estimated_call <= effective_request_limit:
            cleanup_call = llm_calls + 1
            total_calls_hint = max(total_calls_hint, cleanup_call)
            _log(
                f"single-pass final-refinement estimated_call={cleanup_estimated_call} "
                f"draft_tokens={_approx_tokens_text(documentacao)}"
            )
            _emit_progress(
                "call_start",
                is_multi_pass=False,
                current_call=cleanup_call,
                total_calls=max(2, total_calls_hint),
                phase="final_cleanup",
            )
            _ensure_call_limits(cleanup_estimated_call)
            documentacao, call_cost_usd = _invoke_cleanup_pass(
                current_doc_text=documentacao,
                supporting_text=cleanup_supporting_evidence,
            )
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=False,
                current_call=llm_calls,
                total_calls=max(2, total_calls_hint),
                phase="final_cleanup",
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            single_pass_cleanup_done = True
            refinement_done_by_llm = True
            _save_resume_phase("single_cleanup_done", current_doc=documentacao)
        else:
            _log(
                "single-pass final-refinement skipped-llm "
                f"estimated_call={cleanup_estimated_call} exceeds limit={effective_request_limit}; "
                "applying deterministic cleanup only"
            )

        documentacao = _strip_doc_markers(
            documentacao,
            normalize_structure=not single_pass_cleanup_done,
        )
    else:
        files_queue = list(files_for_doc)
        cursor = 0
        extraction_pass = 1
        chunk_budget = effective_request_limit - prompt_overhead_tokens - output_reserve_tokens
        if chunk_budget <= 0:
            raise ValueError(
                "Invalid extraction budget. Increase context window or reduce prompt/output reserves."
            )
        aggregated_pack = _empty_evidence_pack(sections=runtime_sections)
        resume_has_aggregated_pack = False
        if isinstance(resume_state, dict):
            raw_pack = resume_state.get("aggregated_pack")
            if isinstance(raw_pack, dict):
                aggregated_pack = _merge_evidence_packs(
                    aggregated_pack,
                    raw_pack,
                    max_items_per_section=DEFAULT_EVIDENCE_ITEMS_PER_SECTION_TOTAL,
                    sections=runtime_sections,
                )
                resume_has_aggregated_pack = True

        if isinstance(resume_state, dict) and resume_phase == "multi_evidence_extraction":
            try:
                cursor = int(resume_state.get("next_cursor") or 0)
            except Exception:
                cursor = 0
            try:
                extraction_pass = int(resume_state.get("next_extraction_pass") or 1)
            except Exception:
                extraction_pass = 1
            cursor = max(0, min(cursor, len(files_queue)))
            extraction_pass = max(1, extraction_pass)
            _log(
                "resume multi evidence "
                f"cursor={cursor}/{len(files_queue)} "
                f"next_pass={extraction_pass}"
            )
        elif (
            isinstance(resume_state, dict)
            and resume_phase in {"multi_section_writing", "multi_cleanup_ready", "multi_cleanup_done"}
        ):
            if resume_has_aggregated_pack:
                cursor = len(files_queue)
                _log(
                    "resume multi "
                    f"phase={resume_phase} "
                    "skipping evidence extraction"
                )
            else:
                _log(
                    "resume multi state missing aggregated evidence; "
                    "restarting evidence extraction"
                )

        while cursor < len(files_queue):
            files_queue = _ensure_current_item_fits_budget(files_queue, cursor, chunk_budget)
            effective_min_chunk = min_chunk_tokens
            if effective_min_chunk > chunk_budget:
                effective_min_chunk = max(1, chunk_budget // 2)

            chunk_items, next_cursor, chunk_tokens = _take_next_chunk(
                files_queue,
                start_idx=cursor,
                token_budget=chunk_budget,
                min_chunk_tokens=effective_min_chunk,
            )
            if not chunk_items or next_cursor <= cursor:
                raise RuntimeError("Chunk planner failed to advance. Aborting to avoid infinite loop.")

            current_call = llm_calls + 1
            current_chunk_files = max(1, next_cursor - cursor)
            remaining_files = max(0, len(files_queue) - next_cursor)
            remaining_call_estimate = (remaining_files + current_chunk_files - 1) // current_chunk_files
            total_calls_hint = max(
                total_calls_hint,
                current_call + remaining_call_estimate + section_count + 1,  # section writing + cleanup
            )

            chunk_text = _render_repo_content(chunk_items)
            chunk_evidence = _build_repo_evidence_snapshot(chunk_items)
            estimated_call = prompt_overhead_tokens + output_reserve_tokens + chunk_tokens
            _log(
                f"evidence-pass={extraction_pass} "
                f"cursor={cursor}->{next_cursor}/{len(files_queue)} "
                f"chunk_files={len(chunk_items)} "
                f"chunk_tokens={chunk_tokens} "
                f"estimated_call={estimated_call}"
            )
            _emit_progress(
                "call_start",
                is_multi_pass=True,
                current_call=current_call,
                total_calls=total_calls_hint,
                phase="evidence_extraction",
            )
            _ensure_call_limits(estimated_call)
            chunk_pack, call_cost_usd = _invoke_chunk_extraction_pass(
                chunk_text=chunk_text,
                chunk_evidence=chunk_evidence,
            )
            aggregated_pack = _merge_evidence_packs(
                aggregated_pack,
                chunk_pack,
                max_items_per_section=DEFAULT_EVIDENCE_ITEMS_PER_SECTION_TOTAL,
                sections=runtime_sections,
            )
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=True,
                current_call=llm_calls,
                total_calls=total_calls_hint,
                phase="evidence_extraction",
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            cursor = next_cursor
            extraction_pass += 1
            _save_resume_phase(
                "multi_evidence_extraction",
                aggregated_pack=aggregated_pack,
                next_cursor=cursor,
                next_extraction_pass=extraction_pass,
            )

        final_budget_tokens = effective_request_limit - prompt_overhead_tokens - output_reserve_tokens
        global_summary_tokens = _approx_tokens_text(global_summary)
        consolidated_evidence, evidence_items_used, consolidated_evidence_tokens = _fit_consolidated_evidence_to_budget(
            aggregated_pack,
            budget_tokens=final_budget_tokens,
            global_summary_tokens=global_summary_tokens,
            sections=runtime_sections,
        )
        _log(
            "final-writing sectionized "
            f"evidence_items_per_section={evidence_items_used} "
            f"consolidated_tokens={consolidated_evidence_tokens}"
        )
        current_doc = ""
        cleanup_done_by_llm = False
        if isinstance(resume_state, dict) and resume_phase in {"multi_cleanup_ready", "multi_cleanup_done"}:
            resumed_doc = resume_state.get("current_doc")
            if isinstance(resumed_doc, str) and resumed_doc.strip():
                current_doc = resumed_doc
                cleanup_done_by_llm = resume_phase == "multi_cleanup_done"
                _log(
                    "resume multi "
                    f"phase={resume_phase} "
                    f"doc_tokens={_approx_tokens_text(current_doc)}"
                )

        multi_outputs_seed = {}
        multi_start_index = 1
        if isinstance(resume_state, dict) and resume_phase == "multi_section_writing":
            seed = resume_state.get("section_outputs")
            if isinstance(seed, dict):
                multi_outputs_seed = dict(seed)
            try:
                multi_start_index = int(resume_state.get("next_section_index") or 1)
            except Exception:
                multi_start_index = 1

        if not current_doc:
            current_doc, _ = _write_sections_from_context(
                section_context=consolidated_evidence,
                context_tokens=consolidated_evidence_tokens,
                supporting_summary=global_summary,
                is_multi_phase=True,
                phase_name="section_writing",
                log_prefix="multi-pass section-writing",
                initial_section_outputs=multi_outputs_seed,
                start_section_index=multi_start_index,
                checkpoint_phase="multi_section_writing",
                checkpoint_extra=lambda _outputs, _next_idx: {"aggregated_pack": aggregated_pack},
            )
            _save_resume_phase(
                "multi_cleanup_ready",
                aggregated_pack=aggregated_pack,
                current_doc=current_doc,
            )

        cleanup_estimated_call = (
            prompt_overhead_tokens
            + output_reserve_tokens
            + _approx_tokens_text(global_summary)
            + _approx_tokens_text(current_doc)
        )
        if cleanup_done_by_llm:
            pass
        elif cleanup_estimated_call <= effective_request_limit:
            cleanup_call = llm_calls + 1
            total_calls_hint = max(total_calls_hint, cleanup_call)
            _log(
                f"final-refinement global estimated_call={cleanup_estimated_call} "
                f"draft_tokens={_approx_tokens_text(current_doc)}"
            )
            _emit_progress(
                "call_start",
                is_multi_pass=True,
                current_call=cleanup_call,
                total_calls=total_calls_hint,
                phase="final_cleanup",
            )
            _ensure_call_limits(cleanup_estimated_call)
            current_doc, call_cost_usd = _invoke_cleanup_pass(
                current_doc_text=current_doc,
                supporting_text=global_summary,
            )
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=True,
                current_call=llm_calls,
                total_calls=total_calls_hint,
                phase="final_cleanup",
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            cleanup_done_by_llm = True
            refinement_done_by_llm = True
            _save_resume_phase(
                "multi_cleanup_done",
                aggregated_pack=aggregated_pack,
                current_doc=current_doc,
            )
        else:
            _log(
                "final-refinement skipped-llm "
                f"estimated_call={cleanup_estimated_call} exceeds limit={effective_request_limit}; "
                "applying deterministic cleanup only"
            )

        documentacao = _strip_doc_markers(
            current_doc,
            normalize_structure=not cleanup_done_by_llm,
        )

    incomplete_sections = _incomplete_required_sections(documentacao, sections=runtime_sections)
    if incomplete_sections:
        incomplete_csv = ",".join(incomplete_sections)
        _log(f"section-completion needed sections={incomplete_csv}")
        skeleton_doc = _ensure_required_sections_skeleton(documentacao, sections=runtime_sections)
        completion_estimated_call = (
            prompt_overhead_tokens
            + output_reserve_tokens
            + _approx_tokens_text(global_summary)
            + _approx_tokens_text(skeleton_doc)
        )
        if completion_estimated_call <= effective_request_limit:
            completion_call = llm_calls + 1
            total_calls_hint = max(total_calls_hint, completion_call)
            _emit_progress(
                "call_start",
                is_multi_pass=is_multi_pass,
                current_call=completion_call,
                total_calls=total_calls_hint,
                phase="final_cleanup",
            )
            _ensure_call_limits(completion_estimated_call)
            documentacao, call_cost_usd = _invoke_cleanup_pass(
                current_doc_text=skeleton_doc,
                supporting_text=global_summary,
            )
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=is_multi_pass,
                current_call=llm_calls,
                total_calls=total_calls_hint,
                phase="final_cleanup",
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            refinement_done_by_llm = True
            documentacao = _strip_doc_markers(documentacao, normalize_structure=False)
        else:
            _log(
                "section-completion skipped-llm "
                f"estimated_call={completion_estimated_call} exceeds limit={effective_request_limit}; "
                "applying deterministic section fallback"
            )
            documentacao = _fill_incomplete_sections_with_fallback(
                skeleton_doc,
                language=language,
                sections=runtime_sections,
            )
            documentacao = _strip_doc_markers(
                documentacao,
                normalize_structure=not refinement_done_by_llm,
            )

    # Last-resort guard: keep required section skeleton and avoid empty sections.
    still_incomplete = _incomplete_required_sections(documentacao, sections=runtime_sections)
    if still_incomplete:
        documentacao = _fill_incomplete_sections_with_fallback(
            _ensure_required_sections_skeleton(documentacao, sections=runtime_sections),
            language=language,
            sections=runtime_sections,
        )
        documentacao = _strip_doc_markers(
            documentacao,
            normalize_structure=not refinement_done_by_llm,
        )

    if is_functional_doc:
        documentacao = _rewrite_standard_functional_section_titles(documentacao, language)
    else:
        documentacao = _rewrite_standard_section_titles(documentacao, language)
    documentacao = apply_standard_ai_disclaimer(documentacao, language)

    with open(output_md, "w", encoding="utf-8") as file:
        file.write(documentacao)
    _clear_checkpoint_state()
    _emit_progress(
        "done",
        is_multi_pass=is_multi_pass,
        current_call=llm_calls if llm_calls > 0 else 1,
        total_calls=max(total_calls_hint, llm_calls if llm_calls > 0 else 1),
        phase="done",
        total_cost_usd=total_cost_usd,
        cost_available=(cost_samples > 0),
    )
    _log(
        f"done llm_calls={llm_calls} output={output_md} "
        f"total_cost_usd={total_cost_usd:.6f} cost_available={cost_samples > 0}"
    )


def generate_functional_doc(
    input_json,
    output_md="functional_documentation.md",
    language="PT-BR",
    provider="gemini",
    model_name="gemini-2.5-flash",
    api_key=None,
    use_system_key=True,
    context_window_tokens=DEFAULT_CONTEXT_WINDOW_TOKENS,
    prompt_overhead_tokens=DEFAULT_PROMPT_OVERHEAD_TOKENS,
    output_reserve_tokens=DEFAULT_OUTPUT_RESERVE_TOKENS,
    min_chunk_tokens=DEFAULT_MIN_CHUNK_TOKENS,
    hard_total_token_limit=DEFAULT_MAX_TOTAL_TOKENS,
    max_llm_calls=DEFAULT_MAX_LLM_CALLS,
    request_token_cap=None,
    tpm_limit_tokens=None,
    progress_callback=None,
    functional_sections=None,
    resume_from_checkpoint=False,
    checkpoint_path=None,
):
    return generate_doc(
        input_json=input_json,
        output_md=output_md,
        language=language,
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        use_system_key=use_system_key,
        context_window_tokens=context_window_tokens,
        prompt_overhead_tokens=prompt_overhead_tokens,
        output_reserve_tokens=output_reserve_tokens,
        min_chunk_tokens=min_chunk_tokens,
        hard_total_token_limit=hard_total_token_limit,
        max_llm_calls=max_llm_calls,
        request_token_cap=request_token_cap,
        tpm_limit_tokens=tpm_limit_tokens,
        progress_callback=progress_callback,
        documentation_sections=functional_sections,
        resume_from_checkpoint=resume_from_checkpoint,
        checkpoint_path=checkpoint_path,
        documentation_kind="functional",
    )


def generate_functional_doc_from_technical(
    technical_documentation,
    output_md="functional_documentation.md",
    language="PT-BR",
    provider="gemini",
    model_name="gemini-2.5-flash",
    api_key=None,
    use_system_key=True,
    context_window_tokens=DEFAULT_CONTEXT_WINDOW_TOKENS,
    prompt_overhead_tokens=DEFAULT_PROMPT_OVERHEAD_TOKENS,
    output_reserve_tokens=DEFAULT_OUTPUT_RESERVE_TOKENS,
    hard_total_token_limit=DEFAULT_MAX_TOTAL_TOKENS,
    max_llm_calls=DEFAULT_MAX_LLM_CALLS,
    request_token_cap=None,
    tpm_limit_tokens=None,
    progress_callback=None,
    functional_sections=None,
    resume_from_checkpoint=False,
    checkpoint_path=None,
):
    import hashlib
    import json
    import time
    from pathlib import Path
    from langchain_core.output_parsers import StrOutputParser
    from src.llm_utils import init_llm

    def _log(message):
        print(f"[functional_doc_gen] {message}", flush=True)

    def _emit_progress(event, **payload):
        if progress_callback is None:
            return
        data = {"event": event}
        data.update(payload)
        try:
            progress_callback(data)
        except Exception:
            pass

    source_path = None
    if isinstance(technical_documentation, (str, Path)):
        candidate = Path(str(technical_documentation))
        if candidate.exists():
            source_path = candidate.resolve()
            source_text = candidate.read_text(encoding="utf-8")
        else:
            source_text = str(technical_documentation)
    else:
        source_text = str(technical_documentation or "")
    source_text = _strip_ai_disclaimer_variants(source_text).strip()
    if not source_text:
        raise ValueError("Technical documentation source is empty; cannot generate functional documentation.")

    context_window_tokens = int(context_window_tokens)
    prompt_overhead_tokens = int(prompt_overhead_tokens)
    output_reserve_tokens = int(output_reserve_tokens)
    hard_total_token_limit = int(hard_total_token_limit)
    max_llm_calls = int(max_llm_calls)
    resolved_request_token_cap = _resolve_request_token_cap(provider, model_name, request_token_cap)
    resolved_tpm_limit = _resolve_tpm_limit(provider, model_name, tpm_limit_tokens)

    if context_window_tokens <= 0:
        raise ValueError("context_window_tokens must be positive.")
    if hard_total_token_limit <= 0:
        raise ValueError("hard_total_token_limit must be positive.")
    if max_llm_calls <= 0:
        raise ValueError("max_llm_calls must be positive.")

    effective_request_limit = context_window_tokens
    if resolved_request_token_cap is not None:
        effective_request_limit = min(effective_request_limit, resolved_request_token_cap)
    single_pass_budget = effective_request_limit - prompt_overhead_tokens - output_reserve_tokens
    if single_pass_budget <= 0:
        raise ValueError(
            "Invalid token budget configuration. Increase context window or reduce prompt/output reserves."
        )

    tokens_total = _approx_tokens_text(source_text)
    if tokens_total > hard_total_token_limit:
        raise ValueError(
            "Functional documentation source is too large for safe processing: "
            f"{tokens_total} tokens estimated (limit: {hard_total_token_limit})."
        )

    lang_meta = _language_meta(language)
    runtime_sections = _coerce_runtime_sections(
        functional_sections,
        default_sections=FUNCTIONAL_DOCUMENTATION_SECTIONS,
    )
    sections_format = _build_sections_format(sections=runtime_sections)
    section_keys = list(runtime_sections.keys())
    section_count = len(section_keys)
    is_multi_pass = tokens_total > single_pass_budget

    checkpoint_base = source_path.parent if source_path else Path.cwd()
    checkpoint_file = (
        Path(checkpoint_path)
        if checkpoint_path
        else (checkpoint_base / "functional_doc_gen_resume.json")
    )

    def _resume_source_signature():
        if source_path:
            return {
                "source_path": str(source_path),
                "source_mtime": float(source_path.stat().st_mtime),
            }
        digest = hashlib.sha1(source_text.encode("utf-8")).hexdigest()
        return {"source_sha1": digest, "source_len": len(source_text)}

    def _resume_signature():
        return {
            "version": 1,
            "kind": "functional_doc_from_technical",
            **_resume_source_signature(),
            "language": str(language or ""),
            "provider": str(provider or ""),
            "model_name": str(model_name or ""),
            "context_window_tokens": int(context_window_tokens),
            "prompt_overhead_tokens": int(prompt_overhead_tokens),
            "output_reserve_tokens": int(output_reserve_tokens),
            "hard_total_token_limit": int(hard_total_token_limit),
            "max_llm_calls": int(max_llm_calls),
            "request_token_cap": (
                int(resolved_request_token_cap)
                if resolved_request_token_cap is not None
                else None
            ),
            "tpm_limit_tokens": (
                int(resolved_tpm_limit) if resolved_tpm_limit is not None else None
            ),
            "sections": runtime_sections,
        }

    def _save_checkpoint_state(state):
        payload = {
            "version": 1,
            "signature": _resume_signature(),
            "state": state,
            "saved_at": time.time(),
        }
        checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        checkpoint_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def _clear_checkpoint_state():
        try:
            if checkpoint_file.exists():
                checkpoint_file.unlink()
        except Exception:
            pass

    def _load_checkpoint_state():
        if not resume_from_checkpoint:
            return None
        try:
            if not checkpoint_file.exists():
                return None
            payload = json.loads(checkpoint_file.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return None
            if payload.get("signature") != _resume_signature():
                return None
            state = payload.get("state")
            if isinstance(state, dict):
                return state
        except Exception:
            return None
        return None

    llm_calls = 0
    estimated_processing_tokens = 0
    tpm_events = []
    total_calls_hint = 1
    total_cost_usd = 0.0
    cost_samples = 0
    resume_state = _load_checkpoint_state()
    resume_phase = str(resume_state.get("phase") or "") if isinstance(resume_state, dict) else ""
    if resume_state:
        llm_calls = max(0, int(resume_state.get("llm_calls") or 0))
        estimated_processing_tokens = max(0, int(resume_state.get("estimated_processing_tokens") or 0))
        total_calls_hint = max(1, int(resume_state.get("total_calls_hint") or 1))
        total_cost_usd = max(0.0, float(resume_state.get("total_cost_usd") or 0.0))
        cost_samples = max(0, int(resume_state.get("cost_samples") or 0))
        _log(
            "resume-state "
            f"phase={resume_phase or 'none'} "
            f"llm_calls={llm_calls} "
            f"estimated_processing_tokens={estimated_processing_tokens} "
            f"total_cost_usd={total_cost_usd:.6f}"
        )
    else:
        _clear_checkpoint_state()
    total_calls_hint = max(total_calls_hint, llm_calls + 1)

    def _save_resume_phase(phase, **extra):
        state = {
            "phase": str(phase or ""),
            "llm_calls": int(llm_calls),
            "estimated_processing_tokens": int(estimated_processing_tokens),
            "total_calls_hint": int(total_calls_hint),
            "total_cost_usd": float(total_cost_usd),
            "cost_samples": int(cost_samples),
        }
        state.update(extra)
        _save_checkpoint_state(state)

    _log(
        "start "
        f"tokens_total={tokens_total} "
        f"provider={provider} "
        f"model={model_name} "
        f"effective_request_limit={effective_request_limit} "
        f"tpm_limit={resolved_tpm_limit if resolved_tpm_limit is not None else 'none'}"
    )

    if is_multi_pass:
        chunk_hint = _split_text_into_token_chunks(source_text, token_budget=max(1, single_pass_budget))
        total_calls_hint = max(total_calls_hint, len(chunk_hint) + section_count + 1)
        _emit_progress(
            "plan",
            is_multi_pass=True,
            total_calls=total_calls_hint,
            message="Large technical documentation detected. Functional generation may take a few minutes.",
            total_cost_usd=total_cost_usd,
            cost_available=False,
        )
    else:
        total_calls_hint = max(total_calls_hint, section_count + 1)
        _emit_progress(
            "plan",
            is_multi_pass=False,
            total_calls=total_calls_hint,
            message="",
            total_cost_usd=total_cost_usd,
            cost_available=False,
        )

    model = init_llm(
        provider=provider,
        model_name=model_name,
        api_key=api_key,
        use_system_key=use_system_key,
        temperature=0,
    )
    parser = StrOutputParser()

    def _reserve_tpm_capacity(estimated_call_tokens):
        if resolved_tpm_limit is None:
            return
        if estimated_call_tokens > resolved_tpm_limit:
            raise ValueError(
                "Estimated request size exceeds configured TPM cap for a single call. "
                f"Estimated={int(estimated_call_tokens)}, tpm_cap={int(resolved_tpm_limit)}."
            )
        while True:
            now = time.monotonic()
            tpm_events[:] = [(ts, tok) for ts, tok in tpm_events if (now - ts) < 60.0]
            used = sum(tok for _, tok in tpm_events)
            if used + estimated_call_tokens <= resolved_tpm_limit:
                tpm_events.append((now, int(estimated_call_tokens)))
                return
            oldest_ts = tpm_events[0][0] if tpm_events else now
            sleep_for = max(0.05, 60.0 - (now - oldest_ts) + 0.05)
            _log(
                "tpm-wait "
                f"used_last_min={used} "
                f"next_call_tokens={int(estimated_call_tokens)} "
                f"limit={resolved_tpm_limit} "
                f"sleep_s={sleep_for:.2f}"
            )
            time.sleep(sleep_for)

    def _ensure_call_limits(estimated_call_tokens):
        nonlocal llm_calls, estimated_processing_tokens
        if estimated_call_tokens > effective_request_limit:
            raise ValueError(
                "Estimated request size exceeds configured per-call token limit. "
                f"Estimated={int(estimated_call_tokens)}, limit={int(effective_request_limit)}."
            )
        _reserve_tpm_capacity(estimated_call_tokens)
        llm_calls += 1
        if llm_calls > max_llm_calls:
            raise ValueError(f"Aborted for safety: number of LLM calls exceeded limit ({max_llm_calls}).")
        estimated_processing_tokens += max(0, int(estimated_call_tokens))
        if estimated_processing_tokens > hard_total_token_limit:
            raise ValueError(
                f"Aborted for safety: cumulative processing estimate exceeded {hard_total_token_limit} tokens."
            )

    def _register_call_cost(call_cost):
        nonlocal total_cost_usd, cost_samples
        value = _coerce_cost_usd(call_cost)
        if value is None:
            return None
        total_cost_usd += value
        cost_samples += 1
        return value

    chunk_blocks = list(resume_state.get("chunk_blocks") or []) if isinstance(resume_state, dict) else []
    next_chunk_index = int(resume_state.get("next_chunk_index") or 0) if isinstance(resume_state, dict) else 0
    chunks = [source_text]
    if is_multi_pass:
        chunks = _split_text_into_token_chunks(source_text, token_budget=max(1, single_pass_budget))
        if not chunks:
            chunks = [source_text]
        if resume_phase not in {
            "functional_chunk_extraction",
            "functional_section_writing",
            "functional_cleanup_ready",
            "functional_cleanup_done",
        }:
            chunk_blocks = []
            next_chunk_index = 0
        next_chunk_index = max(0, min(next_chunk_index, len(chunks)))
        if resume_phase in {"functional_section_writing", "functional_cleanup_ready", "functional_cleanup_done"}:
            next_chunk_index = len(chunks)

    while is_multi_pass and next_chunk_index < len(chunks):
        chunk_text = chunks[next_chunk_index]
        chunk_tokens = _approx_tokens_text(chunk_text)
        estimated_call = prompt_overhead_tokens + output_reserve_tokens + chunk_tokens
        current_call = llm_calls + 1
        remaining_chunks = max(0, len(chunks) - (next_chunk_index + 1))
        total_calls_hint = max(total_calls_hint, current_call + remaining_chunks + section_count + 1)
        _emit_progress(
            "call_start",
            is_multi_pass=True,
            current_call=current_call,
            total_calls=total_calls_hint,
            phase="functional_chunk_extraction",
        )
        _ensure_call_limits(estimated_call)
        chunk_summary, call_cost_usd = _invoke_functional_chunk_summary_pass(
            model=model,
            parser=parser,
            lang_meta=lang_meta,
            chunk_text=chunk_text,
        )
        chunk_summary = str(chunk_summary or "").strip()
        if chunk_summary:
            if len(chunk_summary) > 48_000:
                chunk_summary = chunk_summary[:48_000].strip()
            chunk_blocks.append(chunk_summary)
        normalized_call_cost = _register_call_cost(call_cost_usd)
        _emit_progress(
            "call_end",
            is_multi_pass=True,
            current_call=llm_calls,
            total_calls=total_calls_hint,
            phase="functional_chunk_extraction",
            call_cost_usd=normalized_call_cost,
            total_cost_usd=total_cost_usd,
            cost_available=(cost_samples > 0),
        )
        next_chunk_index += 1
        _save_resume_phase(
            "functional_chunk_extraction",
            chunk_blocks=chunk_blocks,
            next_chunk_index=next_chunk_index,
        )

    context_budget = max(1, single_pass_budget)
    if is_multi_pass:
        section_context = _compress_text_blocks_to_budget(chunk_blocks, context_budget)
    else:
        section_context = _compress_text_blocks_to_budget([source_text], context_budget)
    section_context_tokens = _approx_tokens_text(section_context)
    if section_context_tokens > context_budget:
        section_context = section_context[: context_budget * 4].strip()
        section_context_tokens = _approx_tokens_text(section_context)

    section_outputs = {}
    next_section_index = 1
    current_doc = ""
    cleanup_done_by_llm = False
    if isinstance(resume_state, dict):
        if resume_phase in {"functional_section_writing", "functional_cleanup_ready", "functional_cleanup_done"}:
            seed = resume_state.get("section_outputs")
            if isinstance(seed, dict):
                section_outputs = dict(seed)
            try:
                next_section_index = int(resume_state.get("next_section_index") or 1)
            except Exception:
                next_section_index = 1
        if resume_phase in {"functional_cleanup_ready", "functional_cleanup_done"}:
            resumed_doc = resume_state.get("current_doc")
            if isinstance(resumed_doc, str) and resumed_doc.strip():
                current_doc = resumed_doc
                cleanup_done_by_llm = resume_phase == "functional_cleanup_done"
    next_section_index = max(1, min(next_section_index, len(section_keys) + 1))

    if not current_doc:
        for section_idx in range(next_section_index, len(section_keys) + 1):
            section_key = section_keys[section_idx - 1]
            current_call = llm_calls + 1
            remaining_section_calls = len(section_keys) - section_idx
            total_calls_hint = max(total_calls_hint, current_call + remaining_section_calls + 1)
            estimated_call = prompt_overhead_tokens + output_reserve_tokens + section_context_tokens
            _emit_progress(
                "call_start",
                is_multi_pass=is_multi_pass,
                current_call=current_call,
                total_calls=total_calls_hint,
                phase="functional_section_writing",
            )
            _ensure_call_limits(estimated_call)
            section_text, call_cost_usd = _invoke_functional_section_doc_from_context_pass(
                model=model,
                parser=parser,
                lang_meta=lang_meta,
                section_key=section_key,
                section_context=section_context,
                sections=runtime_sections,
            )
            section_outputs[section_key] = section_text
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=is_multi_pass,
                current_call=llm_calls,
                total_calls=total_calls_hint,
                phase="functional_section_writing",
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            _save_resume_phase(
                "functional_section_writing",
                chunk_blocks=chunk_blocks,
                next_chunk_index=next_chunk_index,
                section_outputs=section_outputs,
                next_section_index=min(len(section_keys) + 1, section_idx + 1),
            )
        current_doc = _assemble_document_from_sections(
            section_outputs,
            language=language,
            sections=runtime_sections,
        )
        _save_resume_phase(
            "functional_cleanup_ready",
            chunk_blocks=chunk_blocks,
            next_chunk_index=next_chunk_index,
            section_outputs=section_outputs,
            next_section_index=len(section_keys) + 1,
            current_doc=current_doc,
        )

    cleanup_context_budget = max(
        1,
        effective_request_limit
        - prompt_overhead_tokens
        - output_reserve_tokens
        - _approx_tokens_text(current_doc),
    )
    cleanup_context = _compress_text_blocks_to_budget(
        chunk_blocks if is_multi_pass else [source_text],
        cleanup_context_budget,
    )
    cleanup_context_tokens = _approx_tokens_text(cleanup_context)
    cleanup_estimated_call = (
        prompt_overhead_tokens
        + output_reserve_tokens
        + cleanup_context_tokens
        + _approx_tokens_text(current_doc)
    )

    refinement_done_by_llm = False
    if cleanup_done_by_llm:
        pass
    elif cleanup_estimated_call <= effective_request_limit:
        cleanup_call = llm_calls + 1
        total_calls_hint = max(total_calls_hint, cleanup_call)
        _emit_progress(
            "call_start",
            is_multi_pass=is_multi_pass,
            current_call=cleanup_call,
            total_calls=total_calls_hint,
            phase="functional_final_cleanup",
        )
        _ensure_call_limits(cleanup_estimated_call)
        current_doc, call_cost_usd = _invoke_functional_final_cleanup_pass(
            model=model,
            parser=parser,
            lang_meta=lang_meta,
            sections_format=sections_format,
            current_doc=current_doc,
            supporting_context=cleanup_context,
            sections=runtime_sections,
        )
        normalized_call_cost = _register_call_cost(call_cost_usd)
        _emit_progress(
            "call_end",
            is_multi_pass=is_multi_pass,
            current_call=llm_calls,
            total_calls=total_calls_hint,
            phase="functional_final_cleanup",
            call_cost_usd=normalized_call_cost,
            total_cost_usd=total_cost_usd,
            cost_available=(cost_samples > 0),
        )
        refinement_done_by_llm = True
        _save_resume_phase(
            "functional_cleanup_done",
            chunk_blocks=chunk_blocks,
            next_chunk_index=next_chunk_index,
            section_outputs=section_outputs,
            next_section_index=len(section_keys) + 1,
            current_doc=current_doc,
        )
    else:
        _log(
            "functional final-refinement skipped-llm "
            f"estimated_call={cleanup_estimated_call} exceeds limit={effective_request_limit}; "
            "applying deterministic cleanup only"
        )

    documentacao = _strip_intermediate_markers(
        current_doc,
        normalize_structure=not refinement_done_by_llm,
        style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
    )

    incomplete_sections = _incomplete_required_sections(documentacao, sections=runtime_sections)
    if incomplete_sections:
        skeleton_doc = _ensure_required_sections_skeleton(documentacao, sections=runtime_sections)
        completion_estimated_call = (
            prompt_overhead_tokens
            + output_reserve_tokens
            + _approx_tokens_text(skeleton_doc)
        )
        if completion_estimated_call <= effective_request_limit:
            completion_call = llm_calls + 1
            total_calls_hint = max(total_calls_hint, completion_call)
            _emit_progress(
                "call_start",
                is_multi_pass=is_multi_pass,
                current_call=completion_call,
                total_calls=total_calls_hint,
                phase="functional_final_cleanup",
            )
            _ensure_call_limits(completion_estimated_call)
            documentacao, call_cost_usd = _invoke_functional_final_cleanup_pass(
                model=model,
                parser=parser,
                lang_meta=lang_meta,
                sections_format=sections_format,
                current_doc=skeleton_doc,
                supporting_context=cleanup_context,
                sections=runtime_sections,
            )
            normalized_call_cost = _register_call_cost(call_cost_usd)
            _emit_progress(
                "call_end",
                is_multi_pass=is_multi_pass,
                current_call=llm_calls,
                total_calls=total_calls_hint,
                phase="functional_final_cleanup",
                call_cost_usd=normalized_call_cost,
                total_cost_usd=total_cost_usd,
                cost_available=(cost_samples > 0),
            )
            documentacao = _strip_intermediate_markers(
                documentacao,
                normalize_structure=False,
                style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
            )
        else:
            documentacao = _fill_incomplete_sections_with_fallback(
                skeleton_doc,
                language=language,
                sections=runtime_sections,
            )
            documentacao = _strip_intermediate_markers(
                documentacao,
                normalize_structure=False,
                style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
            )

    still_incomplete = _incomplete_required_sections(documentacao, sections=runtime_sections)
    if still_incomplete:
        documentacao = _fill_incomplete_sections_with_fallback(
            _ensure_required_sections_skeleton(documentacao, sections=runtime_sections),
            language=language,
            sections=runtime_sections,
        )
        documentacao = _strip_intermediate_markers(
            documentacao,
            normalize_structure=False,
            style_rules=FUNCTIONAL_SECTION_STYLE_RULES,
        )

    documentacao = _rewrite_standard_functional_section_titles(documentacao, language)
    documentacao = apply_standard_ai_disclaimer(documentacao, language)
    with open(output_md, "w", encoding="utf-8") as file:
        file.write(documentacao)

    _clear_checkpoint_state()
    _emit_progress(
        "done",
        is_multi_pass=is_multi_pass,
        current_call=llm_calls if llm_calls > 0 else 1,
        total_calls=max(total_calls_hint, llm_calls if llm_calls > 0 else 1),
        phase="done",
        total_cost_usd=total_cost_usd,
        cost_available=(cost_samples > 0),
    )
    _log(
        f"done llm_calls={llm_calls} output={output_md} "
        f"total_cost_usd={total_cost_usd:.6f} cost_available={cost_samples > 0}"
    )


def separate_output(
    documentation='documentacao.md',
    documentation_sections=None,
    output_docs_dir="docs",
    keep_chat_file=True,
):
    import os
    from pathlib import Path

    os.makedirs(output_docs_dir, exist_ok=True)
    docs_dir = Path(output_docs_dir)
    runtime_sections = _coerce_runtime_sections(documentation_sections)

    with open(documentation, 'r', encoding='utf-8') as file:
        conteudo = file.read()

    secoes = conteudo.split("<!-- SECTION:")

    secoes_dict = {}

    for secao in secoes[1:]:
        header, *body = secao.split("-->", 1)
        key = header.strip()
        texto = body[0].strip() if body else ""
        secoes_dict[key] = texto

    # Keep only persistent utility docs; refresh generated section files every run.
    for md_file in docs_dir.glob("*.md"):
        if keep_chat_file and md_file.name.lower() == "chat.md":
            continue
        try:
            md_file.unlink()
        except Exception:
            pass

    for key, section in runtime_sections.items():
        output_path = docs_dir / f"{key.lower()}.md"
        with open(output_path, "w", encoding="utf-8") as secao_file:
            secao_file.write(secoes_dict.get(key, ""))


if __name__ == "__main__":
    generate_doc()
    separate_output()
