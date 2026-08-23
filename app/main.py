from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import SimulationResult, Strategy, TrafficState
from app.repositories import get_strategy, latest_traffic_state, save_strategy, save_traffic_state
from app.services.controller import AdaptiveController, SafetyController
from app.services.esp32 import MockESP32Publisher
from app.services.generator import generate_traffic_state
from app.services.simulation import DeterministicSimulator

publisher = MockESP32Publisher()
controller, safety, simulator = AdaptiveController(), SafetyController(), DeterministicSimulator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Smart Traffic Management", version="0.1.0", lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/health")
def health(): return {"status": "ok", "mode": "simulation"}

@app.post("/traffic", response_model=TrafficState)
def ingest_traffic(state: TrafficState, db: Session = Depends(get_db)):
    save_traffic_state(db, state); return state

@app.get("/traffic/latest", response_model=TrafficState)
def get_latest_traffic(db: Session = Depends(get_db)):
    state = latest_traffic_state(db)
    if not state: raise HTTPException(404, "No traffic state recorded")
    return state

@app.post("/traffic/simulate", response_model=TrafficState)
def simulate_traffic(seed: int | None = None, db: Session = Depends(get_db)):
    state = generate_traffic_state(seed); save_traffic_state(db, state); return state

@app.post("/strategies/recommend", response_model=Strategy)
def recommend(state: TrafficState, db: Session = Depends(get_db)):
    strategy = controller.propose(state); save_strategy(db, strategy); return strategy

@app.post("/strategies/{strategy_id}/apply")
def apply(strategy_id: str, state: TrafficState, db: Session = Depends(get_db)):
    strategy = get_strategy(db, strategy_id)
    if not strategy: raise HTTPException(404, "Strategy not found")
    commands = safety.validate(strategy, state)
    for command in commands: publisher.publish(command)
    return {"accepted": True, "commands": commands}

@app.post("/simulation/evaluate", response_model=SimulationResult)
def evaluate(state: TrafficState, strategy: Strategy): return simulator.evaluate(state, strategy)

@app.get("/status")
def status(): return {"publisher": "mock-esp32", "commands_sent": len(publisher.commands), "external_services": "mocked"}

