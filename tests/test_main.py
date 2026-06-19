from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_config():
    client.put("/api/v1/config", json={"key": "theme", "value": "dark"})
    r = client.get("/api/v1/config/theme")
    assert r.status_code == 200
    assert r.json()["value"] == "dark"

