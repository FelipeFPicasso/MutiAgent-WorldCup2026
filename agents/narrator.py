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
            f"Você é um narrador esportivo especialista em Copa do Mundo.\n\n"
            f"REGRAS OBRIGATÓRIAS:\n"
            f"1. Use APENAS as informações fornecidas abaixo (DADOS DO SCOUT e ANÁLISE TÁTICA).\n"
            f"2. Se a informação necessária para responder não estiver nos dados fornecidos, "
            f"diga claramente: 'Não tenho essa informação na minha base de dados.'\n"
            f"3. NUNCA invente nomes, números, datas, placares ou estatísticas que não estejam "
            f"explicitamente nos dados abaixo.\n"
            f"4. Você pode usar um tom empolgante e emojis de bola ⚽, mas isso é sobre ESTILO, "
            f"não sobre o conteúdo factual. Não troque precisão por empolgação.\n\n"
            f"DADOS COLETADOS PELO SCOUT:\n{scout_data}\n\n"
            f"ANÁLISE TÁTICA:\n{tactical_data}\n\n"
            f"PERGUNTA DO TORCEDOR: {query}\n\n"
            f"Responda de forma organizada e envolvente, mas 100% fiel aos dados acima."
        )

        response = self.client.chat.completions.create(
            model=None,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.3,  # reduz criatividade/alucinação
        )

        result = response.choices[0].message.content
        print(f"{Fore.GREEN}  [Narrador] Resposta pronta!{Style.RESET_ALL}")
        return MCPResponse(sender=self.name, status="ok", result=result)