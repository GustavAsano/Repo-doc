import re
import tiktoken

# Chaves sensiveis que devem ter valores mascarados no code.json
SENSITIVE_KEYS = {
    "API_KEY",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
}


def _redact_placeholders(texto: str) -> str:
    # Esconde placeholders sensiveis por chave mantendo o restante da linha intacto
    linhas = texto.splitlines(keepends=True)
    for idx, linha in enumerate(linhas):
        for key in SENSITIVE_KEYS:
            # Formato KEY="..." ou KEY=...
            linha = re.sub(
                rf"(\b{re.escape(key)}\b\s*=\s*)(\"[^\"]*\"|'[^']*'|[^\s#]+)",
                r'\1"<redacted>"',
                linha,
            )
            # Formato YAML/JSON-like: KEY: "..."
            linha = re.sub(
                rf"(\b{re.escape(key)}\b\s*:\s*)(\"[^\"]*\"|'[^']*'|[^\s,#]+)",
                r'\1"<redacted>"',
                linha,
            )
            # Formato shell: export KEY=...
            linha = re.sub(
                rf"(\bexport\s+{re.escape(key)}\b\s*=\s*)(\"[^\"]*\"|'[^']*'|[^\s#]+)",
                r'\1"<redacted>"',
                linha,
                flags=re.IGNORECASE,
            )
        linhas[idx] = linha
    return "".join(linhas)


def code_em_texto(codigo):
    # Preserva linhas e identacao como string unica e aplica mascaramento sensivel
    texto = codigo.replace("\r", "")
    return _redact_placeholders(texto)


def tokens_aprox(codigo):
    # Retorna a contagem aproximada de tokens em um codigo fonte
    enc = tiktoken.get_encoding("cl100k_base")
    tokenized = enc.encode(codigo, disallowed_special=())
    return len(tokenized)
