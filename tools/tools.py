import json
import os
import unicodedata
from rag import retrieve
 
_DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "copa_dataset.json")
 
 
def _load_dataset() -> dict:
    if not hasattr(_load_dataset, "_cache"):
        with open(_DATASET_PATH, "r", encoding="utf-8") as f:
            _load_dataset._cache = json.load(f)
    return _load_dataset._cache
 
 
def _normalize(text: str) -> str:
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode().lower()
 
 
def search_knowledge_base(query: str, n: int = 6) -> str:
    docs = retrieve(query, n_results=n)
    if not docs:
        return "Nenhuma informação encontrada na base de conhecimento."
    return "\n\n".join(docs)
 
 
def calculate_win_probability(team_a: str, team_b: str) -> str:
 
    dataset = _load_dataset()
    titulos_db = dataset.get("titulos_por_pais", {})
 
    key_a = _normalize(team_a)
    key_b = _normalize(team_b)
 
    data_a = titulos_db.get(key_a)
    data_b = titulos_db.get(key_b)
 
    if data_a is None and data_b is None:
        return (
            f"Sem dados históricos para '{team_a}' nem para '{team_b}'.\n"
            f"Países disponíveis: {', '.join(titulos_db.keys())}."
        )
 
    a = data_a["titulos"] if data_a else 0
    b = data_b["titulos"] if data_b else 0
    total = a + b
 
    if total == 0:
        return (
            f"Ambas as seleções ({team_a.title()} e {team_b.title()}) "
            "ainda não venceram uma Copa do Mundo — probabilidade incalculável por títulos."
        )
 
    prob_a = round((a / total) * 100)
    prob_b = 100 - prob_a
 
    anos_a = ", ".join(str(y) for y in (data_a["anos"] if data_a else []))
    anos_b = ", ".join(str(y) for y in (data_b["anos"] if data_b else []))
 
    return (
        f"Probabilidade baseada em títulos históricos:\n"
        f"  {team_a.title()}: {prob_a}%  ({a} título(s){': ' + anos_a if anos_a else ''})\n"
        f"  {team_b.title()}: {prob_b}%  ({b} título(s){': ' + anos_b if anos_b else ''})"
    )
 
 
def filter_stats(category: str) -> str:
 
    dataset = _load_dataset()
    key = _normalize(category)
 
    if any(k in key for k in ("artilheiro", "gol", "scorer", "top")):
        artilheiros = dataset.get("artilheiros", [])
        artilheiros_sorted = sorted(artilheiros, key=lambda x: x["gols"], reverse=True)
 
        linhas = ["Maiores artilheiros da história da Copa do Mundo:"]
        for i, p in enumerate(artilheiros_sorted[:20], start=1):
            copas_str = ", ".join(str(c) for c in p["copas"])
 
            foi_artilheiro = p.get("artilheiro_em", [])
            artilheiro_str = (
                f"  ⭐ Artilheiro da Copa em: {', '.join(str(a) for a in foi_artilheiro)}"
                if foi_artilheiro else ""
            )
 
            linha = f"  {i:>2}. {p['nome']} ({p['pais']}) — {p['gols']} gols  [Copas: {copas_str}]"
            if artilheiro_str:
                linha += f"\n{artilheiro_str}"
            linhas.append(linha)
 
        return "\n".join(linhas)
 
    if any(k in key for k in ("campe", "titulo", "vencedor", "champion")):
        campeoes = dataset.get("campeoes", [])
        campeoes_sorted = sorted(campeoes, key=lambda x: x["titulos"], reverse=True)
 
        linhas = ["Países campeões mundiais:"]
        for c in campeoes_sorted:
            linhas.append(f"\n  {'─'*50}")
            linhas.append(f"  🏆 {c['pais']} — {c['titulos']} título(s)")
            linhas.append(f"     Maior jogador: {c['maior_jogador']}")
            linhas.append(f"     Artilheiro histórico: {c['artilheiro_historico']}")
            linhas.append(f"     Conquistas:")
            for conquista in c.get("conquistas", []):
                linhas.append(
                    f"       • {conquista['ano']} ({conquista['sede']})  "
                    f"vs {conquista['adversario_final']}  {conquista['placar']}\n"
                    f"         🏟️  {conquista['estadio_final']}"
                )
 
        return "\n".join(linhas)
 
    if any(k in key for k in ("estadio", "estadios", "arena", "stadium", "sede")):
        estadios = dataset.get("estadios", [])
 
        campeoes = dataset.get("campeoes", [])
        finais_no_estadio: dict[str, list[str]] = {}
        for c in campeoes:
            for conquista in c.get("conquistas", []):
                nome_estadio = conquista["estadio_final"]
                info = f"{conquista['ano']} (Final: {c['pais']} {conquista['placar']} {conquista['adversario_final']})"
                finais_no_estadio.setdefault(nome_estadio, []).append(info)
 
        linhas = ["Estádios da Copa 2026:"]
        paises_ordem = ["EUA", "México", "Canadá"]
        for pais in paises_ordem:
            linhas.append(f"\n  [{pais}]")
            for e in estadios:
                if e["pais"] != pais:
                    continue
                linha = (
                    f"    • {e['nome']} — {e['cidade']}  "
                    f"(cap. {e['capacidade']:,})  — {e['nota']}"
                )
                linhas.append(linha)
 
                for nome_historico, finais in finais_no_estadio.items():
                    if _normalize(e["nome"]) in _normalize(nome_historico) or \
                       _normalize(nome_historico) in _normalize(e["nome"]):
                        for f_info in finais:
                            linhas.append(f"         🏆 Final histórica: {f_info}")
 
        return "\n".join(linhas)
 
    return (
        f"Categoria '{category}' não encontrada.\n"
        "Tente: artilheiros, campeões, estádios."
    )