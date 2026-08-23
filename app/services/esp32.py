from abc import ABC, abstractmethod
from app.models import SignalCommand


class SignalPublisher(ABC):
    @abstractmethod
    def publish(self, command: SignalCommand) -> None: ...


class MockESP32Publisher(SignalPublisher):
    def __init__(self) -> None:
        self.commands: list[SignalCommand] = []

    def publish(self, command: SignalCommand) -> None:
        self.commands.append(command)

