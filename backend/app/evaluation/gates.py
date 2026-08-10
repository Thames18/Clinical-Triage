from app.evaluation.schemas import (
    BenchmarkReport
)

class BenchmarkGateError(
    RuntimeError
):
    pass

def enforce_safety_gate(
    report: BenchmarkReport
) -> None:

    if report.false_negatives > 0:
        raise BenchmarkGateError(
            "Safety gate failed: "
            "emergency false negatives detected."
        )

    if (
        report.emergency_sensitivity
        < 1.0
    ):
        raise BenchmarkGateError(
            "Safety gate failed: "
            "emergency sensitivity below 100%."
        )