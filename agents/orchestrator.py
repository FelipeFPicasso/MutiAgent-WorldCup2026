from colorama import Fore, Style
from mcp.protocol import MCPBus, MCPMessage
from agents.scout import ScoutAgent
from agents.tactical import TacticalAgent
from agents.narrator import NarratorAgent
from llm_client import get_client
from tools import filter_stats
 
_TACTICAL_KEYWORDS = {
    "probabilidade", "chance", "favorito", "artilheiro", "gol",
    "campeão", "título", "estádio", "análise", "tático", "histórico",
    "vencer", "ganhar", "melhor", "comparar",
}
 
 
def _needs_tactical(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in _TACTICAL_KEYWORDS)
 
 
_TEAMS = [
    "brasil", "argentina", "alemanha", "frança", "itália", "espanha",
    "portugal", "inglaterra", "uruguai", "holanda", "bélgica", "croácia",
    "marrocos", "escócia", "haiti", "japão", "coreia", "méxico", "canadá",
    "eua", "senegal", "noruega", "equador", "dinamarca", "sérvia",
    "colômbia", "turquia", "austrália", "irã", "egito", "argélia", "jordânia",
]
 
_VAGUE = {
    "ela", "eles", "elas", "ele", "esse", "essa", "esses", "essas",
    "outro", "outros", "outra", "outras", "mesmo", "mesma",
}
 
# Palavras-chave para resolver direto via dados estruturados (filter_stats)
_STATS_TITLE_KW = [
    "titulo", "título", "títulos", "titulos",
    "campeão", "campeao", "campeões", "campeoes",
    "mais vezes", "recordista", "venceu mais", "ganhou mais",
    "mais titulos", "mais títulos", "quantos titulos", "quantos títulos",
    "pais com mais", "país com mais", "selecao com mais", "seleção com mais",
    "maior vencedor", "mais copas",
]
_STATS_SCORER_KW = [
    "artilheiro", "artilheiros", "mais gols", "maior artilheiro",
    "goleador", "top scorer", "quem marcou mais",
]
_STATS_STADIUM_KW = [
    "estadio", "estádio", "estadios", "estádios",
    "arena", "sede", "onde joga", "capacidade",
]
 
 
def _try_filter_stats(query: str) -> str | None:
    """Resolve queries de ranking/estatísticas direto do JSON estruturado."""
    q = query.lower()
    if any(w in q for w in _STATS_TITLE_KW):
        return filter_stats("campeões")
    if any(w in q for w in _STATS_SCORER_KW):
        return filter_stats("artilheiros")
    if any(w in q for w in _STATS_STADIUM_KW):
        return filter_stats("estádios")
    return None
 
 
def _rewrite_query(query: str, history: list[dict]) -> str:
    if not history:
        return query
 
    q_lower = query.lower()
    has_vague = any(term in q_lower for term in _VAGUE)
    has_team  = any(t in q_lower for t in _TEAMS)
    is_short  = len(query.split()) < 7
 
    if not has_vague and not (is_short and not has_team):
        return query
 
    mentioned = []
    for msg in history[-4:]:
        for team in _TEAMS:
            if team in msg["content"].lower() and team not in mentioned:
                mentioned.append(team)
 
    if not mentioned:
        return query
 
    teams_ctx = ", ".join(mentioned)
    return f"{query} (contexto: {teams_ctx})"
 
 
class OrchestratorAgent:
 
    def __init__(self, api_key: str = None):
        self.client = get_client(api_key=api_key)
 
        self.bus = MCPBus()
        self.bus.register("scout",    ScoutAgent(self.client).handle)
        self.bus.register("tactical", TacticalAgent(self.client).handle)
        self.bus.register("narrator", NarratorAgent(self.client).handle)
 
    def run(self, query: str, history: list[dict] = None) -> str:
        history = history or []
 
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[Orquestrador] Processando: '{query}'{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
 
        # 1. Tenta resolver direto com dados estruturados (sem RAG)
        direct_data = _try_filter_stats(query)
        if direct_data:
            print(f"{Fore.GREEN}  [Orquestrador] Dados estruturados encontrados — bypassing RAG.{Style.RESET_ALL}")
            scout_data = direct_data
        else:
            # Reescreve query com contexto se necessário
            search_query = _rewrite_query(query, history)
 
            # Adiciona contexto de Copa 2026 se necessário
            if "2026" not in search_query and "copa" not in search_query.lower():
                if not any(w in search_query.lower() for w in ["titulo", "título", "campeão", "campeao", "ganhou", "venceu"]):
                    search_query = search_query + " Copa do Mundo 2026"
 
            scout_response = self.bus.send(MCPMessage(
                sender="orchestrator",
                receiver="scout",
                action="search",
                payload={"query": search_query},
            ))
            scout_data = scout_response.result or "Sem dados do scout."
 
        # 2. Tático — só quando necessário
        tactical_data = ""
        if _needs_tactical(query):
            tactical_response = self.bus.send(MCPMessage(
                sender="orchestrator",
                receiver="tactical",
                action="analyze",
                payload={"query": query, "scout_data": scout_data},
            ))
            tactical_data = tactical_response.result or ""
        else:
            print(f"{Fore.YELLOW}  [Orquestrador] Análise tática desnecessária — pulando.{Style.RESET_ALL}")
 
        # 3. Narrador
        narrator_response = self.bus.send(MCPMessage(
            sender="orchestrator",
            receiver="narrator",
            action="narrate",
            payload={
                "query": query,
                "scout_data": scout_data,
                "tactical_data": tactical_data,
                "history": history[-6:],
            },
        ))
 
        return narrator_response.result or "Não foi possível gerar a resposta."