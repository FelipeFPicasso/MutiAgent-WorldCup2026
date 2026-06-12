from groq import Groq
from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse


class NarratorAgent:
    """
    Agente responsável por transformar os dados coletados
    em uma resposta empolgante no estilo de locutor esportivo.
    """

    def __init__(self, client: Groq):
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

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
        )

        result = response.choices[0].message.content
        print(f"{Fore.GREEN}  [Narrador] Resposta pronta!{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)
