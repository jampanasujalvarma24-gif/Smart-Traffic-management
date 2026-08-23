from app.models import Severity, SignalCommand, Strategy, TrafficState


class AdaptiveController:
    """Deterministic baseline controller; no ML or external service required."""
    min_green_s = 15
    max_green_s = 75

    def propose(self, state: TrafficState) -> Strategy:
        emergency = next((name for name, a in state.approaches.items() if a.emergency_vehicle_present), None)
        if emergency:
            durations = {name: self.min_green_s for name in state.approaches}
            durations[emergency] = self.max_green_s
            return Strategy(name="emergency-priority", phase_durations_s=durations,
                            rationale=f"Emergency vehicle on {emergency}", emergency_priority=True)
        weights = {name: a.vehicle_count + a.queue_length_m / 8 + a.density * 10 for name, a in state.approaches.items()}
        total = sum(weights.values()) or 1
        durations = {name: max(self.min_green_s, min(self.max_green_s, round(120 * weight / total))) for name, weight in weights.items()}
        return Strategy(name="adaptive-density", phase_durations_s=durations,
                        rationale="Green time proportionate to measured demand")


class SafetyController:
    min_green_s = 10
    max_green_s = 90

    def validate(self, strategy: Strategy, state: TrafficState) -> list[SignalCommand]:
        commands = []
        for phase, duration in strategy.phase_durations_s.items():
            safe_duration = max(self.min_green_s, min(self.max_green_s, duration))
            commands.append(SignalCommand(phase=phase, duration_s=safe_duration, reason=strategy.rationale))
        if not commands:
            raise ValueError("A strategy must define at least one phase")
        critical = [i for i in state.incidents if i.severity == Severity.CRITICAL]
        if critical and not strategy.emergency_priority:
            raise ValueError("Critical incidents require explicit priority handling")
        return commands

