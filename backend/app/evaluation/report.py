import argparse

from app.evaluation.evaluator import run_benchmark
from app.evaluation.gates import enforce_safety_gate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default="data/clinical_triage_bench.json",
    )
    args = parser.parse_args()

    report = run_benchmark(args.dataset)
    enforce_safety_gate(report)

    print("ClinicalTriageBench")
    print("===================")
    print(f"Cases: {report.total_cases}")
    print(f"Accuracy: {report.accuracy:.2%}")
    print(f"Emergency sensitivity: {report.emergency_sensitivity:.2%}")
    print(f"Emergency specificity: {report.emergency_specificity:.2%}")
    print(f"False negatives: {report.false_negatives}")
    print(f"False positives: {report.false_positives}")

    for result in report.results:
        status = "PASS" if result.correct else "FAIL"
        print(
            f"{status} {result.case_id}: "
            f"{result.expected_triage} -> {result.predicted_triage}"
        )


if __name__ == "__main__":
    main()
