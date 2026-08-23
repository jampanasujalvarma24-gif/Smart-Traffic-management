from abc import ABC, abstractmethod
from app.models import SimulationResult, Strategy, TrafficState


class ExternalTrafficProvider(ABC):
    @abstractmethod
    def context_for(self, state: TrafficState) -> dict: ...


class ScenarioAnalyzer(ABC):
    @abstractmethod
    def propose(self, state: TrafficState) -> list[Strategy]: ...


class StrategySimulator(ABC):
    @abstractmethod
    def evaluate(self, state: TrafficState, strategy: Strategy) -> SimulationResult: ...


class NullExternalTrafficProvider(ExternalTrafficProvider):
    def context_for(self, state: TrafficState) -> dict:
        return {"source": "mock", "status": "external context unavailable"}


class MockScenarioAnalyzer(ScenarioAnalyzer):
    def propose(self, state: TrafficState) -> list[Strategy]:
        return []

