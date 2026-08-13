from fastapi.testclient import TestClient
from app.core.dependency import get_current_user
from app.main import app

def test_public_health_and_version():
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    response = client.get("/version")
    assert response.status_code == 200
    assert "app_version" in response.json()

def test_triage_does_not_require_authentication():
    client = TestClient(app)

    response = client.post("/triage", json={
        "age": 60,
        "sex": "male",
        "symptoms": ["shortness of breath"],
        "oxygen_saturation": 84,
    })

    assert response.status_code == 200

    data = response.json()

    assert "triage_level" in data
    assert "summary" in data
    assert "risk_score" in data
    assert "confidence" in data

def test_authenticated_emergency_path():
    app.dependency_overrides[get_current_user] = lambda: "test-user"
    try:
        response = TestClient(app).post("/triage", json={
            "age": 60, "sex": "male", "symptoms": ["shortness of breath"],
            "oxygen_saturation": 84, "respiratory_rate": 28, "consciousness": "alert",
            "symptom_duration_hours": 1
        })
        assert response.status_code == 200
        body = response.json()
        assert body["triage_level"] == "EMERGENCY"
        assert body["ai_assisted"] is False
        assert body["assessment_id"]
    finally:
        app.dependency_overrides.clear()

def test_request_id_is_returned():
    response = TestClient(app).get("/health", headers={"X-Request-ID": "week6-test-request"})
    assert response.headers["X-Request-ID"] == "week6-test-request"
