from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_triage_does_not_require_login():
    payload = {
        "age": 45,
        "sex": "male",
        "temperature_c": 37.0,
        "heart_rate": 80,
        "respiratory_rate": 16,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "oxygen_saturation": 98,
        "consciousness": "alert",
        "symptoms": ["headache"],
        "symptom_duration_hours": 4,
        "medical_history": [],
        "medications": [],
        "allergies": [],
    }

    response = client.post("/triage", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "triage_level" in data
    assert "summary" in data
    assert "risk_score" in data
    assert "confidence" in data