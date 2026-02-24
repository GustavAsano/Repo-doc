from collections import defaultdict
import os


def _node_id(item):
    # Id estavel para item do code.json (deve bater com ids do grafo)
    if item.get("tipo") == "file":
        return item.get("path")
    return f'{item.get("path")}::{item.get("tipo")}::{item.get("nome")}'


def _topo_sort(nodes, deps, order_index):
    # Ordenacao topologica com desempate por ordem original
    nodes_set = set(nodes)
    indeg = {n: 0 for n in nodes}
    adj = defaultdict(list)
    for u, v in deps:
        if u not in nodes_set or v not in nodes_set:
            continue
        adj[u].append(v)
        indeg[v] += 1

    # Inicializa lista de nos sem dependencias
    ready = [n for n in nodes if indeg[n] == 0]
    ready.sort(key=lambda n: order_index.get(n, 0))

    result = []
    while ready:
        # Retira o primeiro da fila e reduz indegree dos vizinhos
        n = ready.pop(0)
        result.append(n)
        for m in adj.get(n, []):
            indeg[m] -= 1
            if indeg[m] == 0:
                ready.append(m)
                ready.sort(key=lambda x: order_index.get(x, 0))

    # Se houver ciclo, mantem ordem original para os restantes
    if len(result) < len(nodes):
        for n in nodes:
            if n not in result:
                result.append(n)
    return result


def atribuir_prioridades(codigos, grafo):
    # Atribui prioridade aos itens do code.json
    id_to_items = defaultdict(list)
    item_ids = []
    item_index = {}
    for idx, item in enumerate(codigos):
        item_id = _node_id(item)
        id_to_items[item_id].append(item)
        item_index[id(item)] = idx
        if item_id not in item_ids:
            item_ids.append(item_id)

    # Base de ordem original
    order_index = {item_id: i for i, item_id in enumerate(item_ids)}

    # Separar itens relevantes (ignore=false)
    relevantes = [
        item_id
        for item_id in item_ids
        if any(not it.get("ignore") for it in id_to_items[item_id])
    ]

    # Readme com prioridade 1 (regra global da raiz)
    readme_id = None
    for item_id in relevantes:
        for item in id_to_items[item_id]:
            if item.get("tipo") == "file" and "readme" in (item.get("path") or "").lower():
                readme_id = item_id
                break
        if readme_id:
            break

    if readme_id:
        # Marca prioridade 1 apenas para itens do README (ignore=false)
        for item in id_to_items[readme_id]:
            if not item.get("ignore"):
                item["priority"] = 1
        relevantes = [i for i in relevantes if i != readme_id]
        next_priority = 2
    else:
        next_priority = 1

    # Mapa id -> arquivo
    id_to_file = {i: id_to_items[i][0].get("path") for i in relevantes}

    # Dependencias por calls: callee antes do caller (mantem prioridade correta)
    deps = []
    for edge in grafo.get("edges", []):
        if edge.get("kind") != "calls":
            continue
        origem = edge.get("from")
        destino = edge.get("to")
        if origem in id_to_items and destino in id_to_items:
            if any(not it.get("ignore") for it in id_to_items[origem]) and any(
                not it.get("ignore") for it in id_to_items[destino]
            ):
                # Grafo visual: callee -> caller
                # Para prioridade: callee antes do caller, entao from (callee) vem antes de to (caller)
                deps.append((origem, destino))

    # Dependencias por arquivo (propaga dependencias entre arquivos)
    arquivos = sorted(set(id_to_file.values()))
    deps_arquivo = []
    for a, b in deps:
        fa = id_to_file.get(a)
        fb = id_to_file.get(b)
        if fa and fb and fa != fb:
            deps_arquivo.append((fb, fa))

    # README primeiro dentro de cada diretorio (exceto raiz, que ja tem prioridade 1)
    readme_por_dir = {}
    for path in arquivos:
        nome = os.path.basename(path)
        if nome and "README" in nome.upper():
            dir_rel = os.path.dirname(path).replace("\\", "/")
            if dir_rel:
                readme_por_dir.setdefault(dir_rel, path)
    for dir_rel, readme_path in readme_por_dir.items():
        for path in arquivos:
            if path == readme_path:
                continue
            dir_path = os.path.dirname(path).replace("\\", "/")
            if dir_path == dir_rel:
                deps_arquivo.append((readme_path, path))

    # Ordena arquivos por topologia e desempate por ordem original
    arquivo_order = {f: min(order_index.get(i, 0) for i in relevantes if id_to_file.get(i) == f) for f in arquivos}
    arquivos_ordenados = _topo_sort(arquivos, deps_arquivo, arquivo_order)

    # Ordena itens dentro de cada arquivo (simbolos antes/apos de acordo com deps)
    for arquivo in arquivos_ordenados:
        itens = [i for i in relevantes if id_to_file.get(i) == arquivo]
        deps_intra = [(a, b) for a, b in deps if id_to_file.get(a) == arquivo and id_to_file.get(b) == arquivo]
        itens_ordenados = _topo_sort(itens, deps_intra, order_index)
        for item_id in itens_ordenados:
            # Pode haver varios itens com mesmo id (ex: overloads)
            itens_id = [it for it in id_to_items[item_id] if not it.get("ignore")]
            itens_id.sort(key=lambda it: item_index.get(id(it), 0))
            for item in itens_id:
                item["priority"] = next_priority
                next_priority += 1

    # Itens ignorados sem prioridade
    for item in codigos:
        if item.get("ignore"):
            item["priority"] = 0
