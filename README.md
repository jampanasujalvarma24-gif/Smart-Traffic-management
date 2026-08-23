# Smart Traffic Management System

Milestone 1 is a simulation-first FastAPI backend for an AI/IoT traffic-signal prototype. It runs with no CCTV, ESP32, MQTT broker, Google Maps, MiroFish, or SUMO installation.

## Run

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `/docs` for the interactive API. Start with `POST /traffic/simulate?seed=42`, then send that JSON to `/strategies/recommend` and `/simulation/evaluate`.

## Architecture

`TrafficState -> AdaptiveController -> SafetyController -> MockESP32Publisher` is deterministic and safe for local prototyping. SQLite stores submitted traffic states and recommendations. Future Google Maps, MiroFish, and SUMO/TraCI integrations belong behind the interfaces in `app/services/adapters.py`; the included generator and deterministic simulator keep the project runnable meanwhile.

## Test

```bash
pytest
```

The ESP32 publisher is intentionally in-memory. Replace it with an MQTT implementation only after defining device authentication, topic conventions, and hardware fail-safe behavior.

