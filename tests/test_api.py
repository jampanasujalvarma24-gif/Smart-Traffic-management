from fastapi.testclient import TestClient
from app.main import app


def test_health_and_simulation_flow(tmp_path, monkeypatch):
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        state = client.post("/traffic/simulate?seed=7").json()
        assert len(state["approaches"]) == 4
        strategy = client.post("/strategies/recommend", json=state).json()
        result = client.post("/simulation/evaluate", json={"state": state, "strategy": strategy})
        assert result.status_code == 200

