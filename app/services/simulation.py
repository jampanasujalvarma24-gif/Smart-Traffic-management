from app.models import SimulationResult, Strategy, TrafficState
from app.services.adapters import StrategySimulator


class DeterministicSimulator(StrategySimulator):
    """Metric stub with the same interface a future SUMO/TraCI adapter will use."""
    def evaluate(self, state: TrafficState, strategy: Strategy) -> SimulationResult:
        total_count = sum(a.vehicle_count for a in state.approaches.values())
        max_queue = max((a.queue_length_m for a in state.approaches.values()), default=0)
        green = sum(strategy.phase_durations_s.values()) or 1
        demand = sum(a.density for a in state.approaches.values())
        delay = round(max(0.0, 12 + demand * 20 - green / max(1, len(state.approaches))), 2)
        throughput = max(0, int(total_count * (1.15 if strategy.emergency_priority else 1.0)))
        return SimulationResult(strategy_id=strategy.id, average_delay_s=delay,
                                throughput_vehicles=throughput, max_queue_m=max_queue,
                                score=round(throughput * 2 - delay - max_queue, 2))

