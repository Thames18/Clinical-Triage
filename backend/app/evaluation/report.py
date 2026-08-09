import argparse
import json
from app.evaluation.evaluator import (
    run_benchmark
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default=(
            "backend/data/"
            "clinical_triage_bench.json"
        ),
    )
    args = parser.parse_args()
    report = run_benchmark(
        args.dataset
    )
    print()
    print(
        "ClinicalTriageBench"
    )
    print(
        "==="
    )
    print(
        f"Cases: {report.total_cases}"
    )
    print(
        f"Accuracy: "
        f"{report.accuracy:.2%}"
    )
    print(
        "Emergency sensitivity: "
        f"{report.emergency_sensitivity:.2%}"
    )
    print(
        "Emergency specificity: "
        f"{report.emergency_specificity:.2%}"
    )
    print(
        "False negatives: "
        f"{report.false_negatives}"
    )
    print(
        "False positives: "
        f"{report.false_positives}"
    )
    print()
    for result in report.results:
        status = (
            "PASS"
            if result.correct
            else "FAIL"
        )
        print(
            f"{status} "
            f"{result.case_id}: "
            f"{result.expected_triage} -> "
            f"{result.predicted_triage}"
        )

if __name__ == "__main__":
    main()