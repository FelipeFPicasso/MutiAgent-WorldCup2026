from colorama import Fore, Style
from mcp.protocol import MCPMessage, MCPResponse
from tools import calculate_win_probability, filter_stats


class TacticalAgent:

    def __init__(self, client):
        self.client = client
        self.name = "tactical"

    def handle(self, message: MCPMessage) -> MCPResponse:
        query = message.payload.get("query", "")
        scout_data = message.payload.get("scout_data", "")
        print(f"{Fore.YELLOW}  [Tático] Analisando dados táticos...{Style.RESET_ALL}")

        extra_info = ""

        query_lower = query.lower()
        if "probabilidade" in query_lower or "chance" in query_lower or "favorito" in query_lower:
            times = self._extract_teams(query_lower)
            if len(times) >= 2:
                extra_info = calculate_win_probability(times[0], times[1])

        if any(word in query_lower for word in ["artilheiro", "gol", "campeão", "título", "estádio"]):
            category = "artilheiros" if "artilheiro" in query_lower else \
                       "campeões" if any(w in query_lower for w in ["campeão", "título"]) else \
                       "estádios"
            extra_info += "\n" + filter_stats(category)

        prompt = (
            f"Você é um analista tático de futebol especialista em Copas do Mundo. "
            f"Faça uma análise técnica e tática com base nos dados abaixo.\n\n"
            f"DADOS DO SCOUT:\n{scout_data}\n\n"
            f"DADOS ADICIONAIS:\n{extra_info if extra_info else 'Nenhum dado adicional.'}\n\n"
            f"PERGUNTA: {query}\n\n"
            f"Forneça uma análise tática objetiva em até 3 parágrafos."
        )

        response = self.client.chat.completions.create(
            model=None,  # usa o modelo padrão configurado em llm_client.py (ex: llama3.1)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )

        # Chama a API do GROQ
        #
        # response = self.client.chat.completions.create(
        #     model="llama-3.3-70b-versatile",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=500,
        # )

        result = response.choices[0].message.content
        print(f"{Fore.GREEN}  [Tático] Análise concluída.{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)

    def _extract_teams(self, text: str) -> list[str]:
        known_teams = [
            "brasil", "argentina", "alemanha", "frança", "itália",
            "espanha", "portugal", "england", "inglaterra", "uruguai",
            "holanda", "bélgica", "croácia", "marrocos",
        ]
        return [t for t in known_teams if t in text]