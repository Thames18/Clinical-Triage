from fastapi.testclient import TestClient
from app.core.dependency import get_current_user
from app.main import app

def test_fhir_bundle_mapping():
    app.dependency_overrides[get_current_user] = lambda: "test-user"
    try:
        response = TestClient(app).post(
            "/fhir/triage?patient_id=demo-patient-001",
            json={
                "age": 40, "sex": "female", "symptoms": ["palpitations"],
                "heart_rate": 170, "respiratory_rate": 20,
                "consciousness": "alert", "symptom_duration_hours": 2
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["resourceType"] == "Bundle"
        assert body["type"] == "collection"
        assert any(x["resource"]["resourceType"] == "Observation" for x in body["entry"])
        assert any(x["resource"]["resourceType"] == "ClinicalImpression" for x in body["entry"])
    finally:
        app.dependency_overrides.clear()
