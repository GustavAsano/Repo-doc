from collections import defaultdict
from pathlib import Path


def gerar_calls_txt(codigos, out_dir):
    # Gera relatorio calls.txt com resumo por arquivo e ordem por prioridade
    por_arquivo = defaultdict(list)
    total_tokens = 0
    for item in codigos:
        # Ignora itens marcados como nao relevantes
        if item.get("ignore"):
            continue
        path = item.get("path", "")
        por_arquivo[path].append(item)
        total_tokens += int(item.get("tokens_aprox") or 0)

    # Ordena arquivos pela menor prioridade entre seus itens
    arquivos_validos = sorted(
        por_arquivo.keys(),
        key=lambda p: min(i.get("priority", 0) or 0 for i in por_arquivo[p]),
    )
    total_arquivos = len(arquivos_validos)

    # Cabecalho do resumo
    linhas = []
    linhas.append("RESUMO")
    linhas.append(f"arquivos_relevantes: {total_arquivos}")
    linhas.append(f"tokens_relevantes_total: {total_tokens}")
    linhas.append("---------")

    # Cada bloco lista itens relevantes do arquivo
    for path in arquivos_validos:
        itens = sorted(por_arquivo[path], key=lambda i: i.get("priority", 0) or 0)
        linhas.append(f"arquivo: {path}")
        nomes = []
        for item in itens:
            tipo = item.get("tipo", "")
            nome = item.get("nome")
            if nome:
                nomes.append(f"{tipo}:{nome}")
            else:
                nomes.append(f"{tipo}")
        linhas.append(f"objetos_relevantes: {len(itens)} | " + ", ".join(nomes))
        soma_tokens = sum(int(i.get("tokens_aprox") or 0) for i in itens)
        linhas.append(f"tokens_relevantes: {soma_tokens}")
        linhas.append("-------")

    # Grava arquivo final
    out_path = Path(out_dir) / "calls.txt"
    out_path.write_text("\n".join(linhas), encoding="utf-8")
