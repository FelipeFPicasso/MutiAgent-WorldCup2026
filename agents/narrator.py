from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse


class NarratorAgent:

    def __init__(self, client):
        self.client = client
        self.name = "narrator"

    def handle(self, message: MCPMessage) -> MCPResponse:
        query = message.payload.get("query", "")
        scout_data = message.payload.get("scout_data", "")
        tactical_data = message.payload.get("tactical_data", "")
        print(f"{Fore.MAGENTA}  [Narrador] Gerando resposta final...{Style.RESET_ALL}")

        prompt = (
            f"Você é um narrador esportivo apaixonado, especialista em Copa do Mundo. "
            f"Use linguagem empolgante, expressões de futebol e emojis de bola ⚽. "
            f"Seja informativo mas com emoção de transmissão ao vivo!\n\n"
            f"DADOS COLETADOS PELO SCOUT:\n{scout_data}\n\n"
            f"ANÁLISE TÁTICA:\n{tactical_data}\n\n"
            f"PERGUNTA DO TORCEDOR: {query}\n\n"
            f"Responda de forma completa, empolgante e bem organizada. "
            f"Use emojis, destaque fatos importantes e termine com uma frase de impacto!"
        )

        # --- ATIVO: modelo local via Ollama (definido em llm_client.py) ---
        response = self.client.chat.completions.create(
            model=None,  # usa o modelo padrão configurado em llm_client.py (ex: llama3.1)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
        )

        # --- INATIVO: chamada original via API Groq ---
        # response = self.client.chat.completions.create(
        #     model="llama-3.3-70b-versatile",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=700,
        # )

        result = response.choices[0].message.content
        print(f"{Fore.GREEN}  [Narrador] Resposta pronta!{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)