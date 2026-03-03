import os


def modulo_py_por_caminho(repo, caminho):
    # Converte caminho em nome de modulo Python (baseado no relpath)
    rel = os.path.relpath(caminho, repo)
    sem_ext = os.path.splitext(rel)[0]
    partes = sem_ext.split(os.sep)
    if partes[-1] == "__init__":
        partes = partes[:-1]
    return ".".join([p for p in partes if p])


def mapear_modulos_python(repo, arquivos):
    # Mapa modulo -> arquivo para resolver imports
    mapa = {}
    for caminho in arquivos:
        if caminho.endswith(".py"):
            modulo = modulo_py_por_caminho(repo, caminho)
            if modulo:
                mapa[modulo] = caminho
    return mapa


def resolver_import_python(modulo, mapa_modulos):
    # Resolve import Python para caminho de arquivo (tenta modulo completo e seus prefixos)
    if modulo in mapa_modulos:
        return mapa_modulos[modulo]
    # Resolve pacote base se existir
    partes = modulo.split(".")
    while partes:
        base = ".".join(partes)
        if base in mapa_modulos:
            return mapa_modulos[base]
        partes.pop()
    return None


def resolver_import_caminho(base, import_str, candidatos_ext):
    # Resolve import relativo (ex: ./x) para caminho com extensoes candidatas
    if not import_str:
        return None
    if import_str.startswith("."):
        base_dir = os.path.dirname(base)
        caminho = os.path.normpath(os.path.join(base_dir, import_str))
        # Caso 1: caminho exato existe
        if os.path.isfile(caminho):
            return caminho
        # Caso 2: tenta anexar extensoes candidatas
        for ext in candidatos_ext:
            if os.path.isfile(caminho + ext):
                return caminho + ext
        # Caso 3: tenta index.ext em diretorio
        for ext in candidatos_ext:
            index_path = os.path.join(caminho, "index" + ext)
            if os.path.isfile(index_path):
                return index_path
    return None
