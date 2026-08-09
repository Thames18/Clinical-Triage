from app.evaluation.metrics import (
    calculate_emergency_sensitivity,
    calculate_emergency_specificity )
from app.evaluation.schemas import (
    EvaluationResult )

def make_result(
    expected: bool,
    predicted: bool ) -> EvaluationResult:
    return EvaluationResult(
        case_id="test",
        expected_triage="EMERGENCY"
        if expected
        else "ROUTINE",
        predicted_triage="EMERGENCY"
        if predicted
        else "ROUTINE",

        correct=expected == predicted,
        expected_emergency=expected,
        predicted_emergency=predicted,
        false_negative=(
            expected and not predicted
        ),
        false_positive=(
            not expected and predicted
        ),
        risk_score=0,
        confidence=1.0,
    )

def test_emergency_sensitivity():
    results = [
        make_result(True, True),
        make_result(True, False),
        make_result(False, False),
    ]
    sensitivity = (
        calculate_emergency_sensitivity(
            results
        )
    )
    assert sensitivity == 0.5

def test_emergency_specificity():
    results = [
        make_result(False, False),
        make_result(False, True),
        make_result(True, True),
    ]
    specificity = (
        calculate_emergency_specificity(
            results
        )
    )
    assert specificity == 0.5