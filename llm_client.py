import requests

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.1:latest"


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

    def __init__(self, content: str):
        self.choices = [_FakeChoice(content)]


class _FakeChoice:
    def __init__(self, content: str):
        self.message = _FakeMessage(content)


class _FakeMessage:
    def __init__(self, content: str):
        self.content = content


def get_client(api_key: str = None) -> "LLMClient":
    return LLMClient()