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
  • Quem foi campeão da Copa de 2022?
  • Quantos títulos a Alemanha tem?
  • Quantos gols Messi tem em copas do mundo?
{Fore.CYAN}Comandos:{Style.RESET_ALL}
  • {Fore.WHITE}ajuda{Style.RESET_ALL}  — mostra esta mensagem
  • {Fore.WHITE}sair{Style.RESET_ALL}   — encerra o programa
"""


def main():
    print(BANNER)

    api_key = os.getenv("GROQ_API_KEY")

    print(f"{Fore.CYAN}[Sistema] Inicializando base de conhecimento...{Style.RESET_ALL}")
    ingest_documents()

    print(f"{Fore.CYAN}[Sistema] Carregando agentes (modelo local via Ollama)...{Style.RESET_ALL}")
    orchestrator = OrchestratorAgent(api_key=api_key)

    print(f"\n{Fore.GREEN}[Sistema] Pronto! Digite sua pergunta sobre a Copa 2026.{Style.RESET_ALL}")
    print(HELP_MSG)

    history = []

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
            resposta = orchestrator.run(user_input, history=history)

            history.append({"role": "user",      "content": user_input})
            history.append({"role": "assistant", "content": resposta})
            history = history[-12:]

            print(f"\n{Fore.GREEN}Resposta:{Style.RESET_ALL}\n")
            print(resposta)
            print(f"\n{Fore.WHITE}{'─'*55}{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}[ERRO] {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
