from rag import retrieve


def search_knowledge_base(query: str, n: int = 3) -> str:
    """Busca na base vetorial e retorna os trechos mais relevantes."""
    docs = retrieve(query, n_results=n)
    if not docs:
        return "Nenhuma informação encontrada na base de conhecimento."
    return "\n\n".join(docs)


def calculate_win_probability(team_a: str, team_b: str) -> str:
    """
    Estima probabilidade de vitória com base em títulos históricos.
    Lógica simplificada para fins didáticos.
    """
    titles = {
        "brasil": 5, "alemanha": 4, "itália": 4, "argentina": 3,
        "frança": 2, "uruguai": 2, "inglaterra": 1, "espanha": 1,
        "portugal": 0, "holanda": 0, "bélgica": 0,
    }

    a = titles.get(team_a.lower(), 0)
    b = titles.get(team_b.lower(), 0)
    total = a + b

    if total == 0:
        return f"Sem dados históricos suficientes para calcular probabilidade entre {team_a} e {team_b}."

    prob_a = round((a / total) * 100)
    prob_b = 100 - prob_a

    return (
        f"Probabilidade baseada em títulos históricos:\n"
        f"  {team_a.title()}: {prob_a}%\n"
        f"  {team_b.title()}: {prob_b}%"
    )


def filter_stats(category: str) -> str:
    """Retorna estatísticas filtradas por categoria."""
    stats = {
        "artilheiros": (
            "Maiores artilheiros da história da Copa do Mundo:\n"
            "  1. Miroslav Klose (Alemanha) — 16 gols\n"
            "  2. Ronaldo Fenômeno (Brasil) — 15 gols\n"
            "  3. Gerd Müller (Alemanha) — 14 gols\n"
            "  4. Just Fontaine (França) — 13 gols\n"
            "  5. Pelé (Brasil) — 12 gols"
        ),
        "campeões": (
            "Países campeões mundiais:\n"
            "  Brasil — 5 títulos (1958, 1962, 1970, 1994, 2002)\n"
            "  Alemanha — 4 títulos (1954, 1974, 1990, 2014)\n"
            "  Itália — 4 títulos (1934, 1938, 1982, 2006)\n"
            "  Argentina — 3 títulos (1978, 1986, 2022)\n"
            "  França — 2 títulos (1998, 2018)\n"
            "  Uruguai — 2 títulos (1930, 1950)"
        ),
        "estádios": (
            "Estádios da Copa 2026:\n"
            "  EUA: MetLife Stadium (final), Rose Bowl, AT&T Stadium, SoFi Stadium\n"
            "  México: Estádio Azteca, Estadio Akron\n"
            "  Canadá: BC Place, BMO Field"
        ),
    }

    key = category.lower()
    for k, v in stats.items():
        if k in key or key in k:
            return v

    return f"Categoria '{category}' não encontrada. Tente: artilheiros, campeões, estádios."
