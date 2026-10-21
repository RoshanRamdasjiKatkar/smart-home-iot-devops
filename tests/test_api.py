from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_toggle_state():
    client.get("/set/ON")
    res = client.get("/api/device/status")
    assert res.status_code == 200
    assert res.json()["status"] == "ON"

    client.get("/set/OFF")
    res = client.get("/api/device/status")
    assert res.status_code == 200
    assert res.json()["status"] == "OFF"