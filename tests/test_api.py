from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active", "version": "1.0.0"}

def test_prediction_flow():
    payload = {
        "source_text": "Hello world",
        "translated_text": "Hallo Welt"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "confidence_score" in data
    assert isinstance(data["confidence_score"], float)