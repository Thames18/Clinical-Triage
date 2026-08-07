TRIAGE_LEVELS = [
    "EMERGENCY",
    "URGENT",
    "SAME_DAY",
    "ROUTINE",
    "SELF_CARE",
    "INSUFFICIENT_INFORMATION",
]

# Vital sign thresholds.
# These are intentionally kept in one place so that clinical rules can be versioned and tested independently of the API, it was obtained through online sources.

OXYGEN_EMERGENCY = 90

HEART_RATE_EMERGENCY_HIGH = 150
HEART_RATE_EMERGENCY_LOW = 40

RESPIRATORY_RATE_EMERGENCY_HIGH = 30
RESPIRATORY_RATE_EMERGENCY_LOW = 8

SYSTOLIC_BP_EMERGENCY_LOW = 80

TEMPERATURE_HIGH = 40.0

# Clinical information that is particularly useful for determining triage urgency.

HIGH_RISK_SYMPTOMS = {
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "severe bleeding",
    "seizure",
    "loss of consciousness",
    "stroke symptoms",
    "facial droop",
    "new weakness",
    "new confusion",
    "severe allergic reaction",
    "anaphylaxis",
}

MEDIUM_RISK_SYMPTOMS = {
    "persistent vomiting",
    "moderate abdominal pain",
    "high fever",
    "persistent dizziness",
    "dehydration",
}