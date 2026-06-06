# utils.py — Funções utilitárias (sem I/O, apenas cálculos)

def calcular_estatisticas(dados: dict, secoes: list) -> dict:
    total_album = sum(len(s["figurinhas"]) for s in secoes)
    total_tenho = sum(
        1 for s in secoes for f in s["figurinhas"]
        if dados.get(str(f), {}).get("tenho", False)
    )
    total_repetidas = sum(
        dados.get(str(f), {}).get("repetidas", 0)
        for s in secoes for f in s["figurinhas"]
    )
    return {
        "total_album": total_album,
        "total_tenho": total_tenho,
        "total_faltam": total_album - total_tenho,
        "total_repetidas": total_repetidas,
        "percentual": (total_tenho / total_album * 100) if total_album > 0 else 0,
    }
