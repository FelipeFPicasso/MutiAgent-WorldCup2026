from groq import Groq
from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse
from tools import search_knowledge_base


class ScoutAgent:
    """
    Agente responsável por buscar informações relevantes
    na base de conhecimento via RAG.
    """

    def __init__(self, client: Groq):
        self.client = client
        self.name = "scout"

    def handle(self, message: MCPMessage) -> MCPResponse:
        query = message.payload.get("query", "")
        print(f"{Fore.CYAN}  [Scout] Buscando na base vetorial: '{query}'{Style.RESET_ALL}")

        context = search_knowledge_base(query)

        prompt = (
            f"Você é um especialista em Copa do Mundo. "
            f"Com base nas informações abaixo, responda de forma objetiva e precisa.\n\n"
            f"INFORMAÇÕES RECUPERADAS:\n{context}\n\n"
            f"PERGUNTA: {query}\n\n"
            f"Responda apenas com os fatos encontrados, sem inventar dados."
        )

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )

        result = response.choices[0].message.content
        print(f"{Fore.GREEN}  [Scout] Dados encontrados.{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)
