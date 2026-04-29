from fastapi.testclient import TestClient
from systems.smart_timetable_api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_parse_empty():
    response = client.post("/smart-parse", json={"text": ""})
    assert response.status_code in [400, 422]