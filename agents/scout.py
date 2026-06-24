from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse
from tools import search_knowledge_base


class ScoutAgent:

    def __init__(self, client):
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

        # --- ATIVO: modelo local via Ollama (definido em llm_client.py) ---
        response = self.client.chat.completions.create(
            model=None,  # usa o modelo padrão configurado em llm_client.py (ex: llama3.1)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
        )

        # Chama a API do GROQ
        #
        # response = self.client.chat.completions.create(
        #     model="llama-3.3-70b-versatile",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=400,
        # )

        result = response.choices[0].message.content
        print(f"{Fore.GREEN}  [Scout] Dados encontrados.{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)