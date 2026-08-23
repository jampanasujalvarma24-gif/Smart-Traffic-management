from app.models import ApproachState, TrafficState
from app.services.controller import AdaptiveController, SafetyController


def state(emergency=False):
    return TrafficState(approaches={"north": ApproachState(vehicle_count=20, density=.8, queue_length_m=60, average_speed_kph=10, emergency_vehicle_present=emergency), "south": ApproachState(vehicle_count=3, density=.1, queue_length_m=5, average_speed_kph=30)})


def test_emergency_priority_is_selected():
    strategy = AdaptiveController().propose(state(True))
    assert strategy.emergency_priority and strategy.phase_durations_s["north"] == 75


def test_safety_clamps_durations():
    strategy = AdaptiveController().propose(state())
    strategy.phase_durations_s["north"] = 500
    assert SafetyController().validate(strategy, state())[0].duration_s == 90

