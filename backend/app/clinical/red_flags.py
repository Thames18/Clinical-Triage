from app.schemas.triage import PatientInput
from app.clinical.constants import (
    OXYGEN_EMERGENCY,
    HEART_RATE_EMERGENCY_HIGH,
    HEART_RATE_EMERGENCY_LOW,
    RESPIRATORY_RATE_EMERGENCY_HIGH,
    RESPIRATORY_RATE_EMERGENCY_LOW,
    SYSTOLIC_BP_EMERGENCY_LOW,
    TEMPERATURE_HIGH,
    HIGH_RISK_SYMPTOMS,
)

from app.clinical.models import RedFlag

def detect_red_flags(
    patient: PatientInput,
) -> list[RedFlag]:

    flags: list[RedFlag] = []

    # Oxygen emergency threshold check 

    if (
        patient.oxygen_saturation is not None
        and patient.oxygen_saturation < OXYGEN_EMERGENCY
    ):
        flags.append(
            RedFlag(
                code="LOW_OXYGEN",
                severity="critical",
                title="Critically low oxygen saturation",
                explanation=(
                    "The recorded oxygen saturation is below the configured emergency threshold."
                ),
                evidence=(
                    f"SpO2 = {patient.oxygen_saturation}%"
                ),
            )
        )
    # Heart rate threshold check 

    if (
        patient.heart_rate is not None
        and patient.heart_rate > HEART_RATE_EMERGENCY_HIGH
    ):
        flags.append(
            RedFlag(
                code="SEVERE_TACHYCARDIA",
                severity="critical",
                title="Severely elevated heart rate",
                explanation=(
                    "The recorded heart rate is above the configured emergency threshold."
                ),
                evidence=(
                    f"Heart rate = {patient.heart_rate} bpm"
                ),
            )
        )


    if (
        patient.heart_rate is not None
        and patient.heart_rate < HEART_RATE_EMERGENCY_LOW
    ):

        flags.append(
            RedFlag(
                code="SEVERE_BRADYCARDIA",
                severity="critical",
                title="Severely low heart rate",
                explanation=(
                    "The recorded heart rate is below the configured emergency threshold."
                ),
                evidence=(
                    f"Heart rate = {patient.heart_rate} bpm"
                ),
            )
        )

    # Respiratory rate threshold checker 

    if (
        patient.respiratory_rate is not None
        and patient.respiratory_rate >
        RESPIRATORY_RATE_EMERGENCY_HIGH
    ):

        flags.append(
            RedFlag(
                code="SEVERE_TACHYPNEA",
                severity="critical",
                title="Severely elevated respiratory rate",
                explanation=(
                    "The respiratory rate is markedly elevated."
                ),
                evidence=(
                    f"Respiratory rate = "
                    f"{patient.respiratory_rate}/min"
                ),
            )
        )


    if (
        patient.respiratory_rate is not None
        and patient.respiratory_rate <
        RESPIRATORY_RATE_EMERGENCY_LOW
    ):

        flags.append(
            RedFlag(
                code="SEVERE_BRADYPNEA",
                severity="critical",
                title="Abnormally low respiratory rate",
                explanation=(
                    "The respiratory rate is below the configured emergency threshold."
                ),
                evidence=(
                    f"Respiratory rate = "
                    f"{patient.respiratory_rate}/min"
                ),
            )
        )

    # Blood pressure threshold checker 

    if (
        patient.systolic_bp is not None
        and patient.systolic_bp <
        SYSTOLIC_BP_EMERGENCY_LOW
    ):
        flags.append(
            RedFlag(
                code="SEVERE_HYPOTENSION",
                severity="critical",
                title="Severely low blood pressure",
                explanation=(
                    "The recorded systolic blood pressure is below the configured emergency threshold."
                ),
                evidence=(
                    f"Systolic BP = {patient.systolic_bp} mmHg"
                ),
            )
        )

    # Temperature threshold checker 

    if (
        patient.temperature_c is not None
        and patient.temperature_c >= TEMPERATURE_HIGH
    ):
        flags.append(
            RedFlag(
                code="EXTREME_FEVER",
                severity="high",
                title="Extremely elevated temperature",
                explanation=(
                    "The recorded temperature is markedly elevated."
                ),
                evidence=(
                    f"Temperature = "
                    f"{patient.temperature_c}°C"
                ),
            )
        )

    # Consciousness checker

    if patient.consciousness in {
        "confused",
        "drowsy",
        "unresponsive",
    }:
        severity = (
            "critical"
            if patient.consciousness == "unresponsive"
            else "high"
        )
        flags.append(
            RedFlag(
                code="ALTERED_MENTAL_STATUS",
                severity=severity,
                title="Altered mental status",
                explanation=(
                    "The level of consciousness is not fully awake."
                ),
                evidence=(
                    f"Consciousness = "
                    f"{patient.consciousness}"
                ),
            )
        )

    # Symptoms

    normalized_symptoms = {
        symptom.strip().lower()
        for symptom in patient.symptoms
    }
    for symptom in normalized_symptoms:
        if symptom in HIGH_RISK_SYMPTOMS:
            flags.append(
                RedFlag(
                    code="HIGH_RISK_SYMPTOM",
                    severity="high",
                    title="High-risk symptom reported",
                    explanation=(
                        "The reported symptom may require urgent clinical assessment."
                    ),
                    evidence=f"Symptom = {symptom}",
                )
            )

    return flags