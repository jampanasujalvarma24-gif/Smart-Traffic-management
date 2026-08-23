import random
from app.models import ApproachState, Incident, IncidentType, Severity, TrafficState


def generate_traffic_state(seed: int | None = None) -> TrafficState:
    rng = random.Random(seed)
    approaches = {name: ApproachState(vehicle_count=rng.randint(2, 30), density=round(rng.uniform(.05, .95), 2),
                                      queue_length_m=round(rng.uniform(3, 100), 1), average_speed_kph=round(rng.uniform(5, 45), 1),
                                      emergency_vehicle_present=False)
                  for name in ("north", "south", "east", "west")}
    return TrafficState(approaches=approaches, external_context={"source": "simulation"})

