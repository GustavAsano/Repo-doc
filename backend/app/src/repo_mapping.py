import json
import os

from app.src.code_utils import code_em_texto, tokens_aprox
from app.src.filters import coletar_arquivos
from app.src.graph_build import gerar_grafo, gerar_mmd, gerar_mmd_visual, ordenar_grupos_por_prioridade
from app.src.calls_report import gerar_calls_txt
from app.src.import_resolver import mapear_modulos_python, resolver_import_caminho, resolver_import_python
from app.src.parsers import (
    EXT_TREESITTER,
    HAS_SQLGLOT,
    HAS_TREESITTER,
    parse_js_regex,
    parse_java_regex,
    parse_c_regex,
    parse_python,
    parse_notebook,
    parse_sql,
    parse_treesitter,
    parse_vue,
)
from app.src.priority import atribuir_prioridades


def check_dependencies():
    """Validate that all required dependencies are installed."""
    if not HAS_SQLGLOT or not HAS_TREESITTER:
        raise RuntimeError("Instale dependencias: pip install sqlglot tree_sitter tree_sitter_languages")

def repo_map(repo, output_dir=None):
    """
    Map the given repository and generate artifacts with code and a graph.
    
    Args:
        repo (str): Path to the repository
        output_dir (str, optional): Output directory. If None, uses HUBIA_ARTEFATOS_HOME or current dir
        
    Returns:
        dict: Information about generated files
    """
    # Validate repository
    repo = os.path.abspath(repo)
    if not os.path.isdir(repo):
        raise ValueError("Repositorio invalido.")
    
    # Check dependencies
    check_dependencies()
    
    # Collect files
    arquivos = coletar_arquivos(repo)
    if arquivos and isinstance(arquivos[0], dict):
        arquivos_list = [a["path"] for a in arquivos]
    else:
        arquivos_list = arquivos
    
    mapa_modulos = mapear_modulos_python(repo, arquivos_list)
    
    artefatos = []
    deps = {}
    codigos = []
    calls = []
    simbolos_por_arquivo = {}
    chamadas_pendentes = []

    # Process files
    for item in arquivos:
        if isinstance(item, dict):
            caminho = item["path"]
            rel_path = item["rel"]
            ignore = item["ignore"]
            ignore_motivos = item.get("ignore_motivos", [])
        else:
            caminho = item
            rel_path = os.path.relpath(caminho, repo)
            ignore = False
            ignore_motivos = []
        
        ext = os.path.splitext(caminho)[1].lower()
        info = {"kind": "file", "path": rel_path, "lang": ext.lstrip(".")}
        extras = {}
        symbols = []
        codigo = ""

        if ignore:
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                codigo = f.read()
            artefatos.append(info)
            code_text = code_em_texto(codigo)
            codigos.append(
                {
                    "tipo": "file",
                    "path": rel_path,
                    "code": code_text,
                    "tokens_aprox": tokens_aprox(code_text),
                    "resumo": "",
                    "ignore": True,
                    "ignore_motivos": ignore_motivos,
                }
            )
            continue

        if ext == ".py":
            extras, symbols, codigo = parse_python(caminho)
        elif ext == ".ipynb":
            extras, symbols, codigo = parse_notebook(caminho)
        elif ext == ".sql":
            extras, symbols, codigo = parse_sql(caminho)
        elif ext == ".vue":
            extras, symbols, codigo = parse_vue(caminho)
        elif ext in EXT_TREESITTER:
            extras, symbols, codigo = parse_treesitter(caminho, EXT_TREESITTER[ext])
            if ext == ".java" and not symbols:
                symbols = parse_java_regex(caminho)
            if ext in (".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts") and not symbols:
                symbols = parse_js_regex(caminho)
            if ext in (".c", ".h", ".cpp", ".hpp") and not symbols:
                symbols = parse_c_regex(caminho)
        else:
            with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                codigo = f.read()

        for k, v in extras.items():
            if v:
                info[k] = v

        artefatos.append(info)
        # Sempre salva o arquivo inteiro como item do code.json
        code_text = code_em_texto(codigo)
        codigos.append(
            {
                "tipo": "file",
                "path": rel_path,
                "code": code_text,
                "tokens_aprox": tokens_aprox(code_text),
                "resumo": "",
                "ignore": False,
                "ignore_motivos": ignore_motivos,
            }
        )

        for sym in symbols:
            art = {
                "kind": sym["kind"],
                "name": sym["name"],
                "path": rel_path,
                "lang": info["lang"],
            }
            artefatos.append(art)
            code_text = code_em_texto(sym["code"])
            codigos.append(
                {
                    "tipo": sym["kind"],
                    "nome": sym["name"],
                    "path": rel_path,
                    "code": code_text,
                    "tokens_aprox": tokens_aprox(code_text),
                    "resumo": "",
                    "ignore": False,
                    "ignore_motivos": ignore_motivos,
                }
            )
            sym_id = f'{rel_path}::{sym["kind"]}::{sym["name"]}'
            simbolos_por_arquivo.setdefault(rel_path, {}).setdefault(sym["name"], []).append(sym_id)
            if sym.get("calls"):
                chamadas_pendentes.append({"from": sym_id, "path": rel_path, "calls": sym["calls"]})

        deps[rel_path] = set()
        if ext == ".py":
            for imp in extras.get("imports", []):
                alvo = resolver_import_python(imp, mapa_modulos)
                if alvo:
                    deps[rel_path].add(os.path.relpath(alvo, repo))
        elif ext in (".js", ".jsx", ".ts", ".tsx"):
            for imp in extras.get("imports", []):
                alvo = resolver_import_caminho(caminho, imp, [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"])
                if alvo:
                    deps[rel_path].add(os.path.relpath(alvo, repo))
        elif ext in (".c", ".h", ".cpp", ".hpp"):
            for imp in extras.get("imports", []):
                alvo = resolver_import_caminho(caminho, imp, [".h", ".hpp", ".c", ".cpp"])
                if alvo:
                    deps[rel_path].add(os.path.relpath(alvo, repo))

    # Determine output directory
    if output_dir is None:
        repo_nome = os.path.basename(os.path.normpath(repo))
        base_out = os.environ.get("HUBIA_ARTEFATOS_HOME")
        if not base_out:
            base_out = os.path.abspath(os.path.dirname(__file__))
        output_dir = os.path.join(base_out, "out", repo_nome)
    
    os.makedirs(output_dir, exist_ok=True)

    # Process calls
    for item in chamadas_pendentes:
        for call_name in item["calls"]:
            destinos = simbolos_por_arquivo.get(item["path"], {}).get(call_name, [])
            for dest_id in destinos:
                calls.append({"from": item["from"], "to": dest_id})

    # Gera grafo base (com imports, contains e calls)
    grafo = gerar_grafo(artefatos, deps, calls)
    mmd = gerar_mmd(grafo)

    # Atribui prioridade de leitura e grava artefatos finais
    atribuir_prioridades(codigos, grafo)
    graphs_dir = os.path.join(output_dir, "graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    graph_path = os.path.join(graphs_dir, "graph.json")
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(grafo, f, ensure_ascii=True, indent=2)
    # Visualizacao filtrada (ignore=false) com prioridade
    graph_visual = gerar_mmd_visual(grafo, codigos, include_symbols=True)
    graph_visual_path = os.path.join(graphs_dir, "graph_all.mmd")
    with open(graph_visual_path, "w", encoding="utf-8") as f:
        f.write(graph_visual)
    # Grafos por subpasta seguindo ordem do grafo geral
    graphs_visual_dir = os.path.join(graphs_dir, "visualization")
    os.makedirs(graphs_visual_dir, exist_ok=True)
    grupos_ordenados = ordenar_grupos_por_prioridade(codigos, include_symbols=True)
    graph_sub_files = []
    for grupo in grupos_ordenados:
        graph_sub = gerar_mmd_visual(grafo, codigos, include_symbols=True, group_filter=grupo)
        path_sub = os.path.join(graphs_visual_dir, f"{grupo}.mmd")
        with open(path_sub, "w", encoding="utf-8") as f:
            f.write(graph_sub)
        graph_sub_files.append(path_sub)
    artifacts_path = os.path.join(output_dir, "artifacts.json")
    with open(artifacts_path, "w", encoding="utf-8") as f:
        json.dump(artefatos, f, ensure_ascii=True, indent=2)
    code_path = os.path.join(output_dir, "code.json")
    with open(code_path, "w", encoding="utf-8") as f:
        json.dump(codigos, f, ensure_ascii=True, indent=2)
    gerar_calls_txt(codigos, output_dir)
    calls_path = os.path.join(output_dir, "calls.txt")

    return {
        "output_dir": output_dir,
        "graphs_dir": graphs_dir,
        "graph_file": graph_path,
        "mmd_file": None,
        "graph_visual_file": graph_visual_path,
        "artifacts_file": artifacts_path,
        "code_file": code_path,
        "calls_file": calls_path,
        "graph_sub_files": graph_sub_files,
    }


