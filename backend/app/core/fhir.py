from __future__ import annotations
from datetime import datetime, timezone
from app.schemas.triage import PatientInput, TriageResponse

def _observation(resource_id: str, code: str, display: str, value: float | int, unit: str) -> dict:
    return {
        "resourceType": "Observation",
        "id": resource_id,
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org", "code": code, "display": display}]},
        "valueQuantity": {"value": value, "unit": unit},
    }

def triage_to_fhir_bundle(patient: PatientInput, result: TriageResponse, patient_id: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    entries = [{
        "resource": {
            "resourceType": "Patient",
            "id": patient_id,
            "gender": patient.sex,
        }
    }]

    observations = [
        ("heart_rate", "8867-4", "Heart rate", "beats/min"),
        ("respiratory_rate", "9279-1", "Respiratory rate", "breaths/min"),
        ("oxygen_saturation", "59408-5", "Oxygen saturation", "%"),
        ("temperature_c", "8310-5", "Body temperature", "Cel"),
    ]
    for field, code, display, unit in observations:
        value = getattr(patient, field)
        if value is not None:
            entries.append({"resource": _observation(
                f"{result.assessment_id}-{field}", code, display, value, unit
            )})

    entries.append({"resource": {
        "resourceType": "ClinicalImpression",
        "id": str(result.assessment_id),
        "status": "completed",
        "description": result.summary,
        "effectiveDateTime": now,
        "note": [{"text": f"Triage level: {result.triage_level}. Decision support only; clinician review required."}],
    }})

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "timestamp": now,
        "entry": entries,
    }
