from groq import Groq
from colorama import Fore, Style
from mcp.protocol import MCPBus, MCPMessage
from agents.scout import ScoutAgent
from agents.tactical import TacticalAgent
from agents.narrator import NarratorAgent


class OrchestratorAgent:
    """
    Agente principal. Recebe a pergunta do usuário,
    coordena os demais agentes via MCP e retorna a resposta final.
    """

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.bus = MCPBus()

        scout = ScoutAgent(self.client)
        tactical = TacticalAgent(self.client)
        narrator = NarratorAgent(self.client)

        self.bus.register("scout", scout.handle)
        self.bus.register("tactical", tactical.handle)
        self.bus.register("narrator", narrator.handle)

    def run(self, query: str) -> str:
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[Orquestrador] Processando: '{query}'{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")

        scout_response = self.bus.send(MCPMessage(
            sender="orchestrator",
            receiver="scout",
            action="search",
            payload={"query": query},
        ))

        scout_data = scout_response.result or "Sem dados do scout."

        tactical_response = self.bus.send(MCPMessage(
            sender="orchestrator",
            receiver="tactical",
            action="analyze",
            payload={"query": query, "scout_data": scout_data},
        ))

        tactical_data = tactical_response.result or "Sem análise tática."

        narrator_response = self.bus.send(MCPMessage(
            sender="orchestrator",
            receiver="narrator",
            action="narrate",
            payload={
                "query": query,
                "scout_data": scout_data,
                "tactical_data": tactical_data,
            },
        ))

        return narrator_response.result or "Não foi possível gerar a resposta."
