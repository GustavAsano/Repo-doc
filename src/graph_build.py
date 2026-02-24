def _id_para_artefato(artefato):
    # Id estavel para arquivo ou simbolo (precisa bater com code.json)
    if artefato["kind"] == "file":
        return artefato["path"]
    return f'{artefato["path"]}::{artefato["kind"]}::{artefato["name"]}'


def _id_para_codigo(item):
    # Id estavel a partir de item do code.json
    if item.get("tipo") == "file":
        return item.get("path")
    return f'{item.get("path")}::{item.get("tipo")}::{item.get("nome")}'


def gerar_grafo(artefatos, deps, calls):
    # Grafo simples de dependencias e conteudos
    nodes = []
    edges = []
    edge_set = set()

    for art in artefatos:
        # Cada artefato vira um no com id estavel
        node = {"id": _id_para_artefato(art), "kind": art["kind"]}
        if art["kind"] == "file":
            node["path"] = art["path"]
        else:
            node["name"] = art["name"]
            node["path"] = art["path"]
        nodes.append(node)

    # Imports entre arquivos (deduplicado)
    for origem, destinos in deps.items():
        for dest in destinos:
            key = (origem, dest, "import")
            if key not in edge_set:
                edge_set.add(key)
                edges.append({"from": origem, "to": dest, "kind": "import"})

    # Relacao arquivo -> simbolo (contains)
    for art in artefatos:
        if art["kind"] != "file":
            edges.append(
                {
                    "from": art["path"],
                    "to": _id_para_artefato(art),
                    "kind": "contains",
                }
            )

    # Visualmente: chamado -> chamador
    for call in calls:
        if call["from"] == call["to"]:
            continue
        key = (call["to"], call["from"], "calls")
        if key not in edge_set:
            edge_set.add(key)
            edges.append({"from": call["to"], "to": call["from"], "kind": "calls"})

    return {"nodes": nodes, "edges": edges}


def gerar_mmd(grafo):
    # Exporta Mermaid MMD
    # Layout LR deixa a prioridade mais intuitiva na horizontal
    linhas = [
        "%%{init: {'flowchart': {'nodeSpacing': 60, 'rankSpacing': 80, 'useMaxWidth': false, 'direction': 'LR'}, 'flowchartRenderer': 'elk'}}%%",
        "flowchart LR",
    ]
    linhas.append("direction LR")
    id_por_path = {}
    for i, no in enumerate(grafo["nodes"], start=1):
        node_id = f"N{i}"
        id_por_path[no["id"]] = node_id
        if no["kind"] == "file":
            label = no["path"]
        else:
            label = f'{no["name"]} ({no["kind"]})'
        label = label.replace('"', "'")
        linhas.append(f'{node_id}["{label}"]')
    for aresta in grafo["edges"]:
        a = id_por_path.get(aresta["from"])
        b = id_por_path.get(aresta["to"])
        if a and b:
            linhas.append(f"{a} --> {b}")
    return "\n".join(linhas)


def _group_name_from_path(path):
    parts = (path or "").replace("\\", "/").split("/")
    return parts[0] if len(parts) > 1 else "root"


def _build_id_info(codigos, include_symbols=False, group_filter=None):
    # Monta mapa id -> info, opcionalmente filtrando por grupo
    id_info = {}
    # Mapa auxiliar por arquivo para derivar prioridade quando o "file" nao existe em code.json
    # (mantido apenas se decidirmos usar mais tarde)
    by_path = {}
    for item in codigos:
        if item.get("ignore"):
            continue
        # Opcionalmente limita a arquivos para reduzir ruido visual
        if not include_symbols and item.get("tipo") != "file":
            continue
        item_id = _id_para_codigo(item)
        prioridade = item.get("priority")
        tipo = item.get("tipo")
        nome = item.get("nome")
        path = item.get("path")
        if group_filter and _group_name_from_path(path) != group_filter:
            continue
        id_info[item_id] = {
            "tipo": tipo,
            "nome": nome,
            "path": path,
            "priority": prioridade,
        }
        if path:
            by_path.setdefault(path, []).append(prioridade)
    return id_info


def ordenar_grupos_por_prioridade(codigos, include_symbols=False):
    # Ordena subpastas pela menor prioridade encontrada no grafo geral
    grupos = {}
    for item in codigos:
        if item.get("ignore"):
            continue
        if not include_symbols and item.get("tipo") != "file":
            continue
        path = item.get("path") or ""
        group = _group_name_from_path(path)
        prio = item.get("priority")
        if prio is None:
            continue
        grupos.setdefault(group, []).append(prio)
    ordered = sorted(grupos.items(), key=lambda x: min(x[1]) if x[1] else 10**9)
    return [g for g, _ in ordered]


def gerar_mmd_visual(grafo, codigos, include_symbols=False, group_filter=None):
    # Exporta Mermaid MMD filtrado para ignore=false e com prioridade no label
    id_info = _build_id_info(codigos, include_symbols=include_symbols, group_filter=group_filter)

    # Layout LR deixa a prioridade mais intuitiva na horizontal
    linhas = [
        "%%{init: {'flowchart': {'nodeSpacing': 60, 'rankSpacing': 80, 'useMaxWidth': false, 'direction': 'LR'}, 'flowchartRenderer': 'elk'}}%%",
        "flowchart LR",
    ]
    id_por_path = {}
    idx = 1
    # Agrupa por diretorio de primeiro nivel para reduzir bagunca
    groups = {}
    for item_id, info in id_info.items():
        path = info.get("path") or ""
        group = _group_name_from_path(path)
        groups.setdefault(group, []).append(item_id)

    for group_name in sorted(groups.keys()):
        linhas.append(f'subgraph {group_name}')
        linhas.append("direction LR")
        for item_id in sorted(groups[group_name], key=lambda i: id_info[i].get("priority") or 0):
            node_id = f"N{idx}"
            idx += 1
            id_por_path[item_id] = node_id
            info = id_info[item_id]
            prioridade = info.get("priority")
            if info.get("tipo") == "file":
                label = f'{info.get("path")} [p={prioridade}]'
            else:
                label = f'{info.get("nome")} ({info.get("tipo")}) [p={prioridade}]'
            label = label.replace('"', "'")
            linhas.append(f'{node_id}["{label}"]')
            # Aplica classe para colorir por tipo
            if info.get("tipo") == "file":
                linhas.append(f"class {node_id} file")
            elif info.get("tipo") in {"class", "interface", "enum", "struct", "trait"}:
                linhas.append(f"class {node_id} type")
            elif info.get("tipo") in {"function", "async_function", "method"}:
                linhas.append(f"class {node_id} callable")
            else:
                linhas.append(f"class {node_id} misc")
        linhas.append("end")

    edge_lines = []
    # Arestas reais (import/contains/calls)
    for aresta in grafo["edges"]:
        origem = aresta["from"]
        destino = aresta["to"]
        kind = aresta.get("kind")

        # Quando estamos mostrando apenas arquivos, colapsa calls/contains em nivel de arquivo
        if not include_symbols:
            if kind == "import":
                origem_id = origem
                destino_id = destino
            elif kind in {"calls", "contains"}:
                origem_id = origem.split("::")[0]
                destino_id = destino.split("::")[0]
            else:
                origem_id = origem
                destino_id = destino
        else:
            origem_id = origem
            destino_id = destino

        a = id_por_path.get(origem_id)
        b = id_por_path.get(destino_id)
        if a and b:
            edge_lines.append(f"{a} --> {b}")

    # Arestas invisiveis para ordenar por prioridade da esquerda para a direita
    # Ordena por prioridade; itens sem prioridade vao para o fim
    ordem = sorted(
        ((info["priority"], node_id) for node_id, info in id_info.items() if node_id in id_por_path),
        key=lambda x: (x[0] is None, x[0] or 0, id_por_path.get(x[1], "")),
    )
    order_edges = []
    if ordem:
        ordered_nodes = [id_por_path[node_id] for _, node_id in ordem]
        for i in range(len(ordered_nodes) - 1):
            order_edges.append(f"{ordered_nodes[i]} --> {ordered_nodes[i + 1]}")

    # Emite edges reais primeiro, depois edges de ordenacao
    linhas.extend(edge_lines)
    order_start_index = len(edge_lines)
    linhas.extend(order_edges)

    # Oculta visualmente as arestas de ordenacao (mantem apenas o efeito de layout)
    for i in range(len(order_edges)):
        linhas.append(f"linkStyle {order_start_index + i} stroke-width:0,opacity:0")

    # Definicoes de estilo (cores por tipo)
    linhas.append("classDef file fill:#1f2937,stroke:#94a3b8,color:#e2e8f0")
    linhas.append("classDef type fill:#0f766e,stroke:#5eead4,color:#f0fdfa")
    linhas.append("classDef callable fill:#7c3aed,stroke:#c4b5fd,color:#f5f3ff")
    linhas.append("classDef misc fill:#334155,stroke:#94a3b8,color:#e2e8f0")

    return "\n".join(linhas)
