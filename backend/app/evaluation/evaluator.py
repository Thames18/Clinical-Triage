import json
from pathlib import Path

from app.evaluation.metrics import (
    calculate_emergency_sensitivity,
    calculate_emergency_specificity,
    count_false_negatives,
    count_false_positives,
)
from app.evaluation.schemas import (
    BenchmarkCase,
    BenchmarkReport,
    EvaluationResult,
)
from app.schemas.triage import PatientInput
from app.services.triage_service import analyze_patient


def load_benchmark(path: str) -> list[BenchmarkCase]:
    with Path(path).open("r", encoding="utf-8") as file:
        data = json.load(file)
    return [BenchmarkCase(**case) for case in data]


def evaluate_case(case: BenchmarkCase) -> EvaluationResult:
    result = analyze_patient(PatientInput(**case.patient))
    predicted_emergency = result.triage_level == "EMERGENCY"

    return EvaluationResult(
        case_id=case.case_id,
        expected_triage=case.expected_triage,
        predicted_triage=result.triage_level,
        correct=case.expected_triage == result.triage_level,
        expected_emergency=case.emergency,
        predicted_emergency=predicted_emergency,
        false_negative=case.emergency and not predicted_emergency,
        false_positive=not case.emergency and predicted_emergency,
        risk_score=result.risk_score,
        confidence=result.confidence,
    )


def run_benchmark(path: str) -> BenchmarkReport:
    cases = load_benchmark(path)
    results = [evaluate_case(case) for case in cases]
    total = len(results)
    correct = sum(result.correct for result in results)

    return BenchmarkReport(
        total_cases=total,
        correct=correct,
        accuracy=correct / total if total else 0.0,
        emergency_sensitivity=calculate_emergency_sensitivity(results),
        emergency_specificity=calculate_emergency_specificity(results),
        false_negatives=count_false_negatives(results),
        false_positives=count_false_positives(results),
        results=results,
    )
