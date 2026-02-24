import ast
import json
import re
import warnings

# Dependencias externas solicitadas pelo usuario (podem nao existir no ambiente)
try:
    import sqlglot
    from sqlglot import expressions as sqlglot_exp
except Exception:
    sqlglot = None
    sqlglot_exp = None

try:
    from tree_sitter_languages import get_language, get_parser
except Exception:
    get_language = None
    get_parser = None


# Flags simples para validar dependencias
HAS_SQLGLOT = sqlglot is not None
HAS_TREESITTER = get_parser is not None


# Mapa de extensao -> linguagem do tree-sitter
EXT_TREESITTER = {
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".mts": "typescript",
    ".cts": "typescript",
    ".java": "java",
    ".go": "go",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cs": "c_sharp",
    ".rb": "ruby",
    ".php": "php",
    ".rs": "rust",
}


# Consultas simples para extrair imports/include por linguagem
QUERIES_TREESITTER_IMPORTS = {
    "javascript": "(import_statement source: (string) @source)",
    "typescript": "(import_statement source: (string) @source)",
    "tsx": "(import_statement source: (string) @source)",
    "java": "(import_declaration (scoped_identifier) @source)\n(import_declaration (identifier) @source)",
    "go": "(import_spec path: (interpreted_string_literal) @source)",
    "c": "(preproc_include path: (string_literal) @source)",
    "cpp": "(preproc_include path: (string_literal) @source)",
    "c_sharp": "(using_directive name: (qualified_name) @source)\n(using_directive name: (identifier) @source)",
}


# Consultas para extrair classes/funcoes/etc
QUERIES_TREESITTER_SYMBOLS = {
    "javascript": (
        "(function_declaration) @function\n"
        "(class_declaration) @class\n"
        "(method_definition) @method"
    ),
    "typescript": (
        "(function_declaration) @function\n"
        "(class_declaration) @class\n"
        "(method_definition) @method\n"
        "(interface_declaration) @interface"
    ),
    "tsx": (
        "(function_declaration) @function\n"
        "(class_declaration) @class\n"
        "(method_definition) @method\n"
        "(interface_declaration) @interface"
    ),
    "java": (
        "(class_declaration) @class\n"
        "(interface_declaration) @interface\n"
        "(enum_declaration) @enum\n"
        "(method_declaration) @method"
    ),
    "go": (
        "(function_declaration) @function\n"
        "(method_declaration) @method\n"
        "(type_spec) @type"
    ),
    "c": "(function_definition) @function",
    "cpp": "(function_definition) @function",
    "c_sharp": (
        "(class_declaration) @class\n"
        "(interface_declaration) @interface\n"
        "(struct_declaration) @struct\n"
        "(enum_declaration) @enum\n"
        "(method_declaration) @method"
    ),
    "ruby": (
        "(class) @class\n"
        "(module) @module\n"
        "(method) @method"
    ),
    "php": (
        "(function_definition) @function\n"
        "(class_declaration) @class\n"
        "(interface_declaration) @interface\n"
        "(trait_declaration) @trait"
    ),
    "rust": (
        "(function_item) @function\n"
        "(struct_item) @struct\n"
        "(enum_item) @enum\n"
        "(trait_item) @trait"
    ),
}


TIPOS_TREESITTER_SYMBOLS = {
    "javascript": {
        "function_declaration": "function",
        "class_declaration": "class",
        "method_definition": "method",
    },
    "typescript": {
        "function_declaration": "function",
        "class_declaration": "class",
        "method_definition": "method",
        "interface_declaration": "interface",
    },
    "tsx": {
        "function_declaration": "function",
        "class_declaration": "class",
        "method_definition": "method",
        "interface_declaration": "interface",
    },
    "java": {
        "class_declaration": "class",
        "interface_declaration": "interface",
        "enum_declaration": "enum",
        "method_declaration": "method",
    },
    "go": {
        "function_declaration": "function",
        "method_declaration": "method",
        "type_spec": "type",
    },
    "c": {
        "function_definition": "function",
    },
    "cpp": {
        "function_definition": "function",
    },
    "c_sharp": {
        "class_declaration": "class",
        "interface_declaration": "interface",
        "struct_declaration": "struct",
        "enum_declaration": "enum",
        "method_declaration": "method",
    },
    "ruby": {
        "class": "class",
        "module": "module",
        "method": "method",
    },
    "php": {
        "function_definition": "function",
        "class_declaration": "class",
        "interface_declaration": "interface",
        "trait_declaration": "trait",
    },
    "rust": {
        "function_item": "function",
        "struct_item": "struct",
        "enum_item": "enum",
        "trait_item": "trait",
    },
}


def ler_texto(caminho):
    # Leitura tolerante a erros de encoding
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def limpar_literal(texto):
    # Remove aspas ou <> de literais comuns (imports/paths)
    texto = texto.strip()
    if len(texto) >= 2 and texto[0] == texto[-1] and texto[0] in ("'", '"', "`"):
        return texto[1:-1]
    if texto.startswith("<") and texto.endswith(">"):
        return texto[1:-1]
    return texto


def nome_simbolo(node, codigo):
    # Tenta obter nome via campo "name"
    alvo = node.child_by_field_name("name")
    if alvo:
        return codigo[alvo.start_byte : alvo.end_byte].strip()
    # Fallback simples por tipos comuns quando o campo "name" nao existe
    tipos = {
        "identifier",
        "type_identifier",
        "field_identifier",
        "scoped_identifier",
        "qualified_identifier",
        "constant",
        "name",
        "property_identifier",
    }
    stack = [node]
    while stack:
        atual = stack.pop()
        if atual.type in tipos:
            return codigo[atual.start_byte : atual.end_byte].strip()
        for i in range(atual.named_child_count):
            stack.append(atual.named_child(i))
    return ""


def parse_python(caminho):
    # AST do Python para imports e definicoes
    codigo = ler_texto(caminho)
    try:
        # Evita avisos de SyntaxWarning por escapes invalidos em strings de terceiros
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=SyntaxWarning)
            arvore = ast.parse(codigo, filename=caminho)
    except Exception:
        # Se nao parsear, retorna apenas o codigo inteiro
        return {"imports": []}, [], codigo

    imports = []
    symbols = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            for alias in no.names:
                imports.append(alias.name)
        elif isinstance(no, ast.ImportFrom):
            if no.module:
                imports.append(no.module)
        elif isinstance(no, ast.ClassDef):
            # Classe vira simbolo com trecho do codigo
            trecho = ast.get_source_segment(codigo, no) or ""
            symbols.append({"name": no.name, "kind": "class", "code": trecho})
        elif isinstance(no, ast.FunctionDef):
            # Funcao com coleta simples de chamadas
            trecho = ast.get_source_segment(codigo, no) or ""
            calls = _extract_calls(no)
            symbols.append({"name": no.name, "kind": "function", "code": trecho, "calls": calls})
        elif isinstance(no, ast.AsyncFunctionDef):
            # Funcao async como simbolo proprio
            trecho = ast.get_source_segment(codigo, no) or ""
            calls = _extract_calls(no)
            symbols.append({"name": no.name, "kind": "async_function", "code": trecho, "calls": calls})
    return {"imports": imports}, symbols, codigo


JAVA_CLASS_PATTERN = re.compile(r"\b(class|interface|enum)\s+(\w+)")
JAVA_METHOD_PATTERN = re.compile(
    r"^\s*(?:public|protected|private|static|final|abstract|synchronized|native|\s)*"
    r"(?:[\w\<\>\[\]]+\s+)?(?P<name>\w+)\s*\((?P<params>[^\)]*)\)"
)
JAVA_CALL_PATTERN = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
JAVA_KEYWORDS = {"if", "for", "while", "switch", "catch", "new", "return", "throw", "super", "this"}

JS_CLASS_PATTERN = re.compile(r"\bclass\s+([A-Za-z_$][\w$]*)\b")
JS_FUNCTION_PATTERN = re.compile(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(")
JS_VAR_FUNCTION_PATTERN = re.compile(
    r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?function\b"
)
JS_ARROW_PATTERN = re.compile(
    r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>"
)
JS_EXPORTS_ASSIGN_PATTERN = re.compile(r"\bexports\.([A-Za-z_$][\w$]*)\s*=")
JS_MODULE_EXPORTS_ASSIGN_PATTERN = re.compile(r"\bmodule\.exports(?:\.([A-Za-z_$][\w$]*))?\s*=")
JS_EXPORT_DEFAULT_PATTERN = re.compile(r"\bexport\s+default\b")
JS_EXPORT_DEFAULT_FUNCTION_PATTERN = re.compile(r"\bexport\s+default\s+function\b")
JS_MODULE_EXPORTS_OBJECT_PATTERN = re.compile(r"\bmodule\.exports\s*=\s*\{")
JS_EXPORT_DEFAULT_OBJECT_PATTERN = re.compile(r"\bexport\s+default\s*\{")
JS_DEFINE_EXPORTS_PATTERN = re.compile(r"\bdefine\(\s*function\b")

# Versoes multi-linha para heuristicas mais agressivas (sem depender do repo)
JS_EXPORT_DEFAULT_FUNCTION_BLOCK = re.compile(r"\bexport\s+default\s+function\b", re.MULTILINE)
JS_EXPORT_DEFAULT_OBJECT_BLOCK = re.compile(r"\bexport\s+default\s*\{", re.MULTILINE)
JS_MODULE_EXPORTS_OBJECT_BLOCK = re.compile(r"\bmodule\.exports\s*=\s*\{", re.MULTILINE)
JS_MODULE_EXPORTS_ANY_BLOCK = re.compile(r"\bmodule\.exports\b", re.MULTILINE)
JS_EXPORTS_ASSIGN_BLOCK = re.compile(r"\bexports\.([A-Za-z_$][\w$]*)\s*=", re.MULTILINE)

JS_BLOCK_START = re.compile(r"\{")

C_DECL_PATTERN = re.compile(
    r"^\s*(?!#)(?!typedef\b)(?!struct\b)(?!enum\b)(?!union\b)"
    r"(?:[A-Za-z_]\w*[\s\*]+)+(?P<name>[A-Za-z_]\w*)\s*\([^;]*\)\s*(?P<end>\{|;)"
)

C_DEFINE_PATTERN = re.compile(r"^\s*#\s*define\s+([A-Za-z_]\w*)\b")
C_TYPEDEF_PATTERN = re.compile(r"^\s*typedef\s+.*?\b([A-Za-z_]\w*)\s*;")

# Multi-linha para capturar assinaturas quebradas em varias linhas
C_DECL_PATTERN_MULTI = re.compile(
    r"^\s*(?!#)(?!typedef\b)(?!struct\b)(?!enum\b)(?!union\b)"
    r"(?:[A-Za-z_]\w*[\s\*]+)+(?P<name>[A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?P<end>\{|;)",
    re.MULTILINE | re.DOTALL,
)


def _find_block_span(lines, start_idx):
    # Encontra o bloco com base em chaves (aproximado)
    line = lines[start_idx]
    if "{" not in line:
        return start_idx, start_idx
    depth = 0
    started = False
    for idx in range(start_idx, len(lines)):
        for ch in lines[idx]:
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
        if started and depth <= 0:
            return start_idx, idx
    return start_idx, start_idx


def _find_js_block_span(lines, start_idx):
    # Determina span aproximado de bloco JS (chaves)
    return _find_block_span(lines, start_idx)


def parse_js_regex(caminho):
    # Fallback simples para JS/TS sem tree-sitter
    codigo = ler_texto(caminho)
    return parse_js_regex_code(codigo)


def parse_java_regex(caminho):
    # Fallback simples para Java sem tree-sitter
    codigo = ler_texto(caminho)
    linhas = codigo.splitlines()
    symbols = []
    class_stack = []

    for idx, line in enumerate(linhas):
        class_match = JAVA_CLASS_PATTERN.search(line)
        if class_match:
            kind = class_match.group(1)
            name = class_match.group(2)
            start, end = _find_block_span(linhas, idx)
            trecho = "\n".join(linhas[start : end + 1])
            symbols.append({"name": name, "kind": kind, "code": trecho})
            class_stack.append(name)
            continue

        method_match = JAVA_METHOD_PATTERN.match(line)
        if method_match:
            name = method_match.group("name")
            if name and name not in {"if", "for", "while", "switch", "catch"}:
                start, end = _find_block_span(linhas, idx)
                trecho = "\n".join(linhas[start : end + 1])
                calls = []
                for match in JAVA_CALL_PATTERN.finditer(trecho):
                    call_name = match.group(1)
                    if call_name not in JAVA_KEYWORDS:
                        calls.append(call_name)
                symbols.append({"name": name, "kind": "method", "code": trecho, "calls": calls})

    return symbols


def parse_c_regex(caminho):
    # Fallback simples para C/C++ sem tree-sitter (definicoes, prototipos e macros basicos)
    codigo = ler_texto(caminho)
    linhas = codigo.splitlines()
    symbols = []

    for idx, line in enumerate(linhas):
        define_match = C_DEFINE_PATTERN.match(line)
        if define_match:
            name = define_match.group(1)
            symbols.append({"name": name, "kind": "macro", "code": line.strip()})
            continue
        typedef_match = C_TYPEDEF_PATTERN.match(line)
        if typedef_match:
            name = typedef_match.group(1)
            symbols.append({"name": name, "kind": "typedef", "code": line.strip()})
            continue

    # Procura declaracoes/definicoes multi-linha no codigo inteiro
    for match in C_DECL_PATTERN_MULTI.finditer(codigo):
        name = match.group("name")
        end_token = match.group("end")
        # Reconstitui trecho usando a funcao de bloco baseada em linhas
        line_start = codigo[: match.start()].count("\n")
        if end_token == "{":
            start, end = _find_block_span(linhas, line_start)
            trecho = "\n".join(linhas[start : end + 1])
        else:
            # Pega apenas a linha de assinatura
            trecho = linhas[line_start].strip() if line_start < len(linhas) else codigo[match.start() : match.end()]
        symbols.append({"name": name, "kind": "function", "code": trecho})
    return symbols


def _extract_calls(node: ast.AST) -> list:
    # Coleta chamadas simples em AST Python
    calls = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name):
                calls.append(func.id)
            elif isinstance(func, ast.Attribute):
                calls.append(func.attr)
    return calls


def parse_sql(caminho):
    # SQL via sqlglot para extrair tabelas
    codigo = ler_texto(caminho)
    tabelas = []
    if sqlglot and sqlglot_exp:
        try:
            arvore = sqlglot.parse_one(codigo)
            for t in arvore.find_all(sqlglot_exp.Table):
                if t.name:
                    tabelas.append(t.name)
        except Exception:
            pass
    return {"tables": tabelas}, [], codigo


def _nb_source_to_text(value):
    if isinstance(value, list):
        return "".join(str(part) for part in value)
    if value is None:
        return ""
    return str(value)


def _nb_output_to_text(output):
    if not isinstance(output, dict):
        return ""
    output_type = output.get("output_type", "")
    chunks = []
    if output_type == "stream":
        chunks.append(_nb_source_to_text(output.get("text", "")))
    elif output_type in {"display_data", "execute_result"}:
        data = output.get("data") or {}
        for key in ("text/markdown", "text/plain", "text/html"):
            value = data.get(key)
            if value:
                chunks.append(_nb_source_to_text(value))
                break
    elif output_type == "error":
        name = output.get("ename") or "Error"
        value = output.get("evalue") or ""
        chunks.append(f"{name}: {value}".strip(": "))
        traceback = _nb_source_to_text(output.get("traceback", ""))
        if traceback:
            chunks.append(traceback)
    text = "\n".join(chunk.strip() for chunk in chunks if chunk).strip()
    if len(text) > 2500:
        return text[:2500] + "\n...[output truncated]..."
    return text


def _extract_python_imports_from_code(code_text):
    imports = []
    import_pattern = re.compile(r"^\s*import\s+([A-Za-z_][\w\.]*)", re.MULTILINE)
    from_pattern = re.compile(r"^\s*from\s+([A-Za-z_][\w\.]*)\s+import\s+", re.MULTILINE)
    for match in import_pattern.finditer(code_text):
        imports.append(match.group(1))
    for match in from_pattern.finditer(code_text):
        imports.append(match.group(1))
    return imports


def parse_notebook(caminho):
    # Parse de notebooks Jupyter preservando markdown/codigo/outputs textuais.
    raw = ler_texto(caminho)
    try:
        notebook = json.loads(raw)
    except Exception:
        return {"imports": [], "notebook": True, "cells": 0}, [], raw

    metadata = notebook.get("metadata", {}) if isinstance(notebook, dict) else {}
    kernelspec = metadata.get("kernelspec", {}) if isinstance(metadata, dict) else {}
    language_info = metadata.get("language_info", {}) if isinstance(metadata, dict) else {}
    kernel_name = kernelspec.get("name") if isinstance(kernelspec, dict) else None
    language_name = language_info.get("name") if isinstance(language_info, dict) else None

    cells = notebook.get("cells", []) if isinstance(notebook, dict) else []
    if not isinstance(cells, list):
        cells = []

    imports = []
    parts = []
    if kernel_name or language_name:
        parts.append("## Notebook Metadata")
        if kernel_name:
            parts.append(f"- Kernel: {kernel_name}")
        if language_name:
            parts.append(f"- Language: {language_name}")

    for idx, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            continue
        cell_type = (cell.get("cell_type") or "unknown").strip().lower()
        source_text = _nb_source_to_text(cell.get("source", "")).strip()

        if cell_type == "markdown":
            parts.append(f"## Markdown Cell {idx}")
            if source_text:
                parts.append(source_text)
            continue

        if cell_type == "code":
            parts.append(f"## Code Cell {idx}")
            if source_text:
                parts.append(source_text)
                imports.extend(_extract_python_imports_from_code(source_text))

            output_chunks = []
            outputs = cell.get("outputs", [])
            if isinstance(outputs, list):
                for out_idx, output in enumerate(outputs, start=1):
                    out_text = _nb_output_to_text(output)
                    if out_text:
                        output_chunks.append(f"[Output {out_idx}]\n{out_text}")
            if output_chunks:
                parts.append("### Outputs")
                parts.extend(output_chunks)
            continue

        parts.append(f"## {cell_type.capitalize()} Cell {idx}")
        if source_text:
            parts.append(source_text)

    content = "\n\n".join(part for part in parts if part).strip()
    if not content:
        content = raw
    unique_imports = sorted(set(imports))
    extras = {"imports": unique_imports, "notebook": True, "cells": len(cells)}
    return extras, [], content


def parse_treesitter(caminho, linguagem):
    # Tree-sitter para outras linguagens
    codigo = ler_texto(caminho)
    return parse_treesitter_code(linguagem, codigo)


def parse_treesitter_code(linguagem, codigo):
    # Tree-sitter para codigo em memoria
    imports = []
    symbols = []
    if get_parser and get_language:
        try:
            parser = get_parser(linguagem)
            tree = parser.parse(bytes(codigo, "utf-8"))

            # Coleta imports com query especifica por linguagem
            query_str = QUERIES_TREESITTER_IMPORTS.get(linguagem)
            if query_str:
                query = get_language(linguagem).query(query_str)
                for node, _ in query.captures(tree.root_node):
                    texto = codigo[node.start_byte : node.end_byte]
                    imports.append(limpar_literal(texto))

            # Coleta simbolos com query especifica
            query_sym = QUERIES_TREESITTER_SYMBOLS.get(linguagem)
            if query_sym:
                query = get_language(linguagem).query(query_sym)
                for node, cap in query.captures(tree.root_node):
                    nome = nome_simbolo(node, codigo)
                    trecho = codigo[node.start_byte : node.end_byte]
                    if nome:
                        symbols.append({"name": nome, "kind": cap, "code": trecho})

            # Fallback: varredura por tipo de no quando query falha
            if not symbols:
                tipos = TIPOS_TREESITTER_SYMBOLS.get(linguagem, {})
                if tipos:
                    stack = [tree.root_node]
                    while stack:
                        atual = stack.pop()
                        kind = tipos.get(atual.type)
                        if kind:
                            nome = nome_simbolo(atual, codigo)
                            if nome:
                                trecho = codigo[atual.start_byte : atual.end_byte]
                                symbols.append({"name": nome, "kind": kind, "code": trecho})
                        for i in range(atual.named_child_count):
                            stack.append(atual.named_child(i))
        except Exception:
            # Falha silenciosa: retorna listas vazias
            pass
    return {"imports": imports}, symbols, codigo


VUE_SCRIPT_PATTERN = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.IGNORECASE | re.DOTALL)
VUE_LANG_PATTERN = re.compile(r'lang\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)


def _parse_js_ts_code(codigo, linguagem):
    # Seleciona parser JS/TS para codigo em memoria
    if linguagem in {"typescript", "tsx"}:
        extras, symbols, _ = parse_treesitter_code(linguagem, codigo)
    else:
        extras, symbols, _ = parse_treesitter_code("javascript", codigo)
        if not symbols:
            symbols = parse_js_regex_code(codigo)
    return extras, symbols


def parse_js_regex_code(codigo):
    # Fallback simples para JS/TS em codigo em memoria
    linhas = codigo.splitlines()
    symbols = []
    for idx, line in enumerate(linhas):
        name = None
        kind = None
        class_match = JS_CLASS_PATTERN.search(line)
        func_match = JS_FUNCTION_PATTERN.search(line)
        var_func_match = JS_VAR_FUNCTION_PATTERN.search(line)
        arrow_match = JS_ARROW_PATTERN.search(line)
        exports_match = JS_EXPORTS_ASSIGN_PATTERN.search(line)
        module_exports_match = JS_MODULE_EXPORTS_ASSIGN_PATTERN.search(line)
        export_default_match = JS_EXPORT_DEFAULT_PATTERN.search(line)
        export_default_func_match = JS_EXPORT_DEFAULT_FUNCTION_PATTERN.search(line)
        module_exports_object_match = JS_MODULE_EXPORTS_OBJECT_PATTERN.search(line)
        export_default_object_match = JS_EXPORT_DEFAULT_OBJECT_PATTERN.search(line)
        define_exports_match = JS_DEFINE_EXPORTS_PATTERN.search(line)
        if class_match:
            name = class_match.group(1)
            kind = "class"
        elif func_match:
            name = func_match.group(1)
            kind = "function"
        elif var_func_match:
            name = var_func_match.group(1)
            kind = "function"
        elif arrow_match:
            name = arrow_match.group(1)
            kind = "function"
        elif exports_match:
            name = exports_match.group(1)
            kind = "export"
        elif module_exports_match:
            name = module_exports_match.group(1) or "module.exports"
            kind = "export"
        elif export_default_func_match:
            name = "default_export"
            kind = "function"
        elif module_exports_object_match:
            name = "module.exports"
            kind = "object"
        elif export_default_object_match:
            name = "default_export"
            kind = "object"
        elif export_default_match:
            name = "default_export"
            kind = "export"
        elif define_exports_match:
            name = "define"
            kind = "module"
        if not name or not kind:
            continue
        start, end = _find_js_block_span(linhas, idx)
        trecho = "\n".join(linhas[start : end + 1])
        symbols.append({"name": name, "kind": kind, "code": trecho})

    # Heuristicas multi-linha para exports/objects (nao dependem do repo)
    def _append_symbol(name, kind, pos):
        line_idx = codigo[:pos].count("\n")
        if 0 <= line_idx < len(linhas):
            trecho = linhas[line_idx].strip()
        else:
            trecho = codigo[pos : pos + 120]
        symbols.append({"name": name, "kind": kind, "code": trecho})

    for match in JS_EXPORT_DEFAULT_FUNCTION_BLOCK.finditer(codigo):
        _append_symbol("default_export", "function", match.start())
    for match in JS_EXPORT_DEFAULT_OBJECT_BLOCK.finditer(codigo):
        _append_symbol("default_export", "object", match.start())
    for match in JS_MODULE_EXPORTS_OBJECT_BLOCK.finditer(codigo):
        _append_symbol("module.exports", "object", match.start())
    for match in JS_MODULE_EXPORTS_ANY_BLOCK.finditer(codigo):
        _append_symbol("module.exports", "export", match.start())
    for match in JS_EXPORTS_ASSIGN_BLOCK.finditer(codigo):
        _append_symbol(match.group(1), "export", match.start())

    return symbols


def parse_vue(caminho):
    # Parser generico para .vue: extrai <script> e reusa JS/TS
    codigo = ler_texto(caminho)
    imports = []
    symbols = []
    for match in VUE_SCRIPT_PATTERN.finditer(codigo):
        attrs = match.group(1) or ""
        script_code = match.group(2) or ""
        lang = "javascript"
        lang_match = VUE_LANG_PATTERN.search(attrs)
        if lang_match:
            lang = lang_match.group(1).lower()
        if lang in {"ts", "tsx"}:
            extras, syms = _parse_js_ts_code(script_code, "typescript" if lang == "ts" else "tsx")
        else:
            extras, syms = _parse_js_ts_code(script_code, "javascript")
        imports.extend(extras.get("imports", []))
        symbols.extend(syms)
    return {"imports": imports}, symbols, codigo
