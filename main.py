import os
import sys
from dotenv import load_dotenv
from colorama import init, Fore, Style

load_dotenv()
init(autoreset=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag import ingest_documents
from agents.orchestrator import OrchestratorAgent

BANNER = f"""
{Fore.YELLOW}
    ASSISTENTE MULTIAGENTE — COPA DO MUNDO 2026
{Fore.WHITE}  Powered by LLaMA (local via Ollama) · RAG · MCP · Agentes Especializados
{Fore.YELLOW}{'='*55}
{Style.RESET_ALL}"""

HELP_MSG = f"""
{Fore.CYAN}Exemplos de perguntas:{Style.RESET_ALL}
  • Qual é o histórico do Brasil na Copa do Mundo?
  • Quem são os maiores artilheiros da história?
  • Quais são os estádios da Copa 2026?
  • Qual a probabilidade de Brasil vencer a Argentina?
  • Como foi a final da Copa 2022?
  • Quantos títulos a Alemanha tem?

{Fore.CYAN}Comandos:{Style.RESET_ALL}
  • {Fore.WHITE}ajuda{Style.RESET_ALL}  — mostra esta mensagem
  • {Fore.WHITE}sair{Style.RESET_ALL}   — encerra o programa
"""


def main():
    print(BANNER)

    # --- ATIVO: modelo local via Ollama, não requer chave de API ---
    # 'api_key' é repassado apenas por compatibilidade com a assinatura
    # anterior do OrchestratorAgent; o cliente local (llm_client.py) o ignora.
    api_key = os.getenv("GROQ_API_KEY")  # opcional; mantido por compatibilidade

    # --- INATIVO: verificação obrigatória da GROQ_API_KEY (API externa) ---
    # if not api_key:
    #     print(f"{Fore.RED}[ERRO] GROQ_API_KEY não encontrada!")
    #     print(f"Crie um arquivo .env com: GROQ_API_KEY=sua_chave_aqui")
    #     print(f"Obtenha sua chave gratuita em: https://console.groq.com{Style.RESET_ALL}")
    #     sys.exit(1)

    print(f"{Fore.CYAN}[Sistema] Inicializando base de conhecimento...{Style.RESET_ALL}")
    ingest_documents()

    print(f"{Fore.CYAN}[Sistema] Carregando agentes (modelo local via Ollama)...{Style.RESET_ALL}")
    orchestrator = OrchestratorAgent(api_key=api_key)

    print(f"\n{Fore.GREEN}[Sistema] Pronto! Digite sua pergunta sobre a Copa 2026.{Style.RESET_ALL}")
    print(HELP_MSG)

    while True:
        try:
            user_input = input(f"{Fore.YELLOW}Você:{Style.RESET_ALL} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Tamo junto, volte sempre!{Style.RESET_ALL}")
            break

        if not user_input:
            continue

        if user_input.lower() in ("sair", "exit", "quit"):
            print(f"{Fore.YELLOW}Tamo junto, volte sempre!{Style.RESET_ALL}")
            break

        if user_input.lower() in ("ajuda", "help", "?"):
            print(HELP_MSG)
            continue

        try:
            resposta = orchestrator.run(user_input)
            print(f"\n{Fore.GREEN}Resposta:{Style.RESET_ALL}\n")
            print(resposta)
            print(f"\n{Fore.WHITE}{'─'*55}{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}[ERRO] {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()