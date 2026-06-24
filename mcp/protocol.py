from dataclasses import dataclass, field
from typing import Any


@dataclass
class MCPMessage:
    sender: str
    receiver: str
    action: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPResponse:
    sender: str
    status: str
    result: Any = None
    error: str = None


class MCPBus:

    def __init__(self):
        self._handlers: dict[str, callable] = {}
        self.log: list[MCPMessage] = []

    def register(self, agent_name: str, handler: callable):
        self._handlers[agent_name] = handler

    def send(self, message: MCPMessage) -> MCPResponse:
        self.log.append(message)
        handler = self._handlers.get(message.receiver)
        if handler is None:
            return MCPResponse(
                sender="bus",
                status="error",
                error=f"Agente '{message.receiver}' não encontrado.",
            )
        return handler(message)
