from datetime import datetime, timezone
from enum import Enum
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class IncidentType(str, Enum):
    ACCIDENT = "possible_accident"
    STOPPED_VEHICLE = "stopped_vehicle"
    OBSTRUCTION = "road_obstruction"
    ABNORMAL_BEHAVIOUR = "abnormal_behaviour"
    CROWD = "unusual_crowd"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Incident(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: IncidentType
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    approach_id: str
    detected_at: datetime = Field(default_factory=utcnow)
    description: str | None = None


class ApproachState(BaseModel):
    vehicle_count: int = Field(ge=0)
    density: float = Field(ge=0, le=1)
    queue_length_m: float = Field(ge=0)
    average_speed_kph: float = Field(ge=0)
    emergency_vehicle_present: bool = False


class TrafficState(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    id: str = Field(default_factory=lambda: str(uuid4()))
    intersection_id: str = "demo-intersection"
    observed_at: datetime = Field(default_factory=utcnow)
    approaches: dict[str, ApproachState]
    incidents: list[Incident] = Field(default_factory=list)
    external_context: dict[str, str | float | int] = Field(default_factory=dict)


class Strategy(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    phase_durations_s: dict[str, int]
    rationale: str
    emergency_priority: bool = False
    created_at: datetime = Field(default_factory=utcnow)


class SimulationResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    strategy_id: str
    average_delay_s: float = Field(ge=0)
    throughput_vehicles: int = Field(ge=0)
    max_queue_m: float = Field(ge=0)
    score: float
    simulated_at: datetime = Field(default_factory=utcnow)


class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    level: Severity
    message: str
    source: str
    created_at: datetime = Field(default_factory=utcnow)


class SignalCommand(BaseModel):
    phase: str
    duration_s: int
    reason: str

