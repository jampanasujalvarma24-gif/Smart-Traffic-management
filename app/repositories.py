import json
from sqlalchemy.orm import Session
from app.database import StrategyRecord, TrafficStateRecord
from app.models import Strategy, TrafficState


def save_traffic_state(db: Session, state: TrafficState) -> None:
    db.merge(TrafficStateRecord(id=state.id, observed_at=state.observed_at, payload=state.model_dump_json()))
    db.commit()


def latest_traffic_state(db: Session) -> TrafficState | None:
    row = db.query(TrafficStateRecord).order_by(TrafficStateRecord.observed_at.desc()).first()
    return TrafficState.model_validate_json(row.payload) if row else None


def save_strategy(db: Session, strategy: Strategy) -> None:
    db.merge(StrategyRecord(id=strategy.id, created_at=strategy.created_at, payload=strategy.model_dump_json()))
    db.commit()


def get_strategy(db: Session, strategy_id: str) -> Strategy | None:
    row = db.get(StrategyRecord, strategy_id)
    return Strategy.model_validate_json(row.payload) if row else None

