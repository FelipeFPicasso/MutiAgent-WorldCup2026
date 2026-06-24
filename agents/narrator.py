from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse


class NarratorAgent:

    def __init__(self, client):
        self.client = client
        self.name = "narrator"

    def handle(self, message: MCPMessage) -> MCPResponse:
        query         = message.payload.get("query", "")
        scout_data    = message.payload.get("scout_data", "")
        tactical_data = message.payload.get("tactical_data", "")
        history       = message.payload.get("history", [])

        print(f"{Fore.MAGENTA}  [Narrador] Gerando resposta final...{Style.RESET_ALL}")

        # Monta bloco de histórico recente (se houver)
        history_block = ""
        if history:
            lines = []
            for msg in history:
                role = "Usuário" if msg["role"] == "user" else "Assistente"
                lines.append(f"{role}: {msg['content']}")
            history_block = "CONVERSA ANTERIOR:\n" + "\n".join(lines) + "\n\n"

        # Monta contexto de dados
        context_parts = [f"DADOS:\n{scout_data}"]
        if tactical_data.strip():
            context_parts.append(f"ANÁLISE:\n{tactical_data}")
        context = "\n\n".join(context_parts)

        prompt = (
            f"Você é um assistente de Copa do Mundo. Responda em português.\n"
            f"Use SOMENTE os dados abaixo. NÃO diga que não tem informação se a resposta estiver nos dados.\n\n"
            f"DADOS:\n{scout_data}\n\n"
            f"PERGUNTA: {query}\n\n"
            f"Encontre a resposta nos DADOS acima e responda diretamente em 1-2 frases:"
        )

        response = self.client.chat.completions.create(
            model=None,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.1,
        )

        result = response.choices[0].message.content.strip()
        print(f"{Fore.GREEN}  [Narrador] Resposta pronta!{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)
