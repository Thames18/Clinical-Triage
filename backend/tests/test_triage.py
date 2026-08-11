import pytest
from app.services.triage_service import analyze_patient
from app.schemas.triage import PatientInput
from pydantic import ValidationError

def test_low_oxygen():
    patient=PatientInput(
        age=60,
        sex="female",   
        symptoms=[
            "shortness of breath"
        ],
        oxygen_saturation=85
    )
    result=analyze_patient(patient)
    assert (
        result.triage_level
        ==
        "EMERGENCY"
    )
def test_sex_must_be_male_or_female():
    with pytest.raises(ValidationError):
        PatientInput(
            age=30,
            sex="other",
            symptoms=["headache"],
        )

def test_male_is_valid_sex():
    patient = PatientInput(
        age=30,
        sex="male",
        symptoms=["headache"],
    )

    assert patient.sex == "male"


def test_female_is_valid_sex():
    patient = PatientInput(
        age=30,
        sex="female",
        symptoms=["headache"],
    )

    assert patient.sex == "female"