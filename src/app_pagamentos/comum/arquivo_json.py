import json
from pathlib import Path
from typing import Any


def ler_lista_json(caminho: Path) -> list[dict[str, Any]]:
    if not caminho.exists():
        return []

    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erro:
        raise RuntimeError(f"Não foi possível ler {caminho}: {erro}") from erro

    if not isinstance(dados, list) or any(not isinstance(item, dict) for item in dados):
        raise RuntimeError(f"O arquivo {caminho} precisa conter uma lista de registros.")
    return dados


def gravar_lista_json(caminho: Path, dados: list[dict[str, Any]]) -> None:
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as erro:
        raise RuntimeError(f"Não foi possível salvar {caminho}: {erro}") from erro
