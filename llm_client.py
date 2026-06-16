import requests


#
# Pré-requisitos:
#   1. Instalar o Ollama: https://ollama.com
#   2. Baixar um modelo local, por exemplo:
#        ollama pull llama3.1
#      (ou llama3.2, llama3, mistral, etc.)
#   3. O serviço do Ollama deve estar rodando localmente
#      (por padrão em http://localhost:11434)
#
# Não é necessária nenhuma chave de API.

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:3b"


class LLMClient:

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url
        self.model = model
        self.chat = _Chat(self)


class _Chat:
    def __init__(self, parent: "LLMClient"):
        self.completions = _Completions(parent)


class _Completions:
    def __init__(self, parent: "LLMClient"):
        self._parent = parent

    def create(self, model: str = None, messages: list[dict] = None,
           max_tokens: int = 500, **kwargs):

        payload = {
            "model": model or self._parent.model,
            "prompt": messages[-1]["content"],
            "stream": False,
        }

        try:
            resp = requests.post(
                f"{self._parent.base_url}/api/generate",
                json=payload,
                timeout=120,
            )

            resp.raise_for_status()

            data = resp.json()
            content = data.get("response", "")

        except requests.exceptions.ConnectionError:
            content = (
                f"[ERRO] Não foi possível conectar ao Ollama em "
                f"{self._parent.base_url}"
            )

        except Exception as e:
            content = f"[ERRO] Falha na chamada ao modelo local: {e}"

        return _FakeResponse(content)


class _FakeResponse:
    """Imita a estrutura de resposta da API da Groq/OpenAI."""

    def __init__(self, content: str):
        self.choices = [_FakeChoice(content)]


class _FakeChoice:
    def __init__(self, content: str):
        self.message = _FakeMessage(content)


class _FakeMessage:
    def __init__(self, content: str):
        self.content = content


def get_client(api_key: str = None) -> "LLMClient":
    """
    Ponto único de criação do cliente LLM usado pelo OrchestratorAgent.

    O parâmetro api_key é mantido por compatibilidade com a assinatura
    anterior (OrchestratorAgent(api_key=...)), mas não é utilizado pelo
    Ollama. Caso o projeto volte a usar a Groq, descomente o bloco abaixo.
    """
    return LLMClient()


# =============================================================================
# GROQ (API EXTERNA) — INATIVO / MANTIDO COMO REFERÊNCIA
# =============================================================================
#
# from groq import Groq
#
# def get_client(api_key: str = None) -> "Groq":
#     return Groq(api_key=api_key)
#
# Para reativar:
#   1. Comente a classe LLMClient e a função get_client() acima (bloco Ollama).
#   2. Descomente as duas linhas acima.
#   3. Garanta que GROQ_API_KEY esteja definida no arquivo .env.
#   4. Em main.py, restaure a verificação de GROQ_API_KEY (também comentada).
# =============================================================================
