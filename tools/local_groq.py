from __future__ import annotations

class LocalGroq:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.chat = self.Chat()

    class Chat:
        class Completions:
            @staticmethod
            def create(model: str, messages: list[dict], max_tokens: int = 200):
                # Build a simple mock response by echoing the prompt's beginning.
                user_content = ""
                if messages and isinstance(messages, list):
                    user_content = messages[0].get("content", "")

                snippet = user_content[:1000]
                content = (
                    "[LOCAL MOCK RESPONSE]\n"
                    f"Model: {model}\n\n"
                    "Este é um resultado simulado para execução local.\n\n"
                    "Entrada (trecho):\n"
                    f"{snippet}\n\n"
                    "-- FIM DA RESPOSTA SIMULADA --"
                )

                class Message:
                    def __init__(self, content: str):
                        self.content = content

                class Choice:
                    def __init__(self, message: Message):
                        self.message = message

                class Response:
                    def __init__(self, choices: list[Choice]):
                        self.choices = choices

                return Response([Choice(Message(content))])

        def __init__(self):
            self.completions = LocalGroq.Chat.Completions()
