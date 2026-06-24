from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse
from tools import search_knowledge_base


class ScoutAgent:

    def __init__(self, client=None):
        self.client = client
        self.name = "scout"

    def handle(self, message: MCPMessage) -> MCPResponse:
        query = message.payload.get("query", "")
        print(f"{Fore.CYAN}  [Scout] Buscando na base vetorial: '{query}'{Style.RESET_ALL}")

        context = search_knowledge_base(query)

        if not context or not context.strip():
            print(f"{Fore.YELLOW}  [Scout] Nenhum dado relevante encontrado.{Style.RESET_ALL}")
            result = "NENHUMA_INFORMACAO_ENCONTRADA"
        else:
            result = context
            print(f"{Fore.GREEN}  [Scout] Dados encontrados.{Style.RESET_ALL}")

        return MCPResponse(sender=self.name, status="ok", result=result)