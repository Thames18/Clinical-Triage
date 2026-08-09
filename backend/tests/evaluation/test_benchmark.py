from pathlib import Path
from app.evaluation.evaluator import (
    load_benchmark,
    evaluate_case
)

BENCHMARK_PATH = (
    Path(__file__).parents[2]
    / "data"
    / "clinical_triage_bench.json"
)

def test_benchmark_loads():
    cases = load_benchmark(
        str(BENCHMARK_PATH)
    )
    assert len(cases) >= 5

def test_all_emergency_cases_are_detected():
    cases = load_benchmark(
        str(BENCHMARK_PATH)
    )
    emergency_cases = [
        case
        for case in cases
        if case.emergency
    ]
    for case in emergency_cases:
        result = evaluate_case(
            case
        )
        assert (
            result.predicted_emergency
        ), (
            f"Emergency regression: "
            f"{case.case_id}"
        )