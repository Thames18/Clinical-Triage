from app.evaluation.schemas import (
    EvaluationResult
)

def calculate_emergency_sensitivity(
    results: list[EvaluationResult]) -> float:

    actual_emergencies = [
        result
        for result in results
        if result.expected_emergency
    ]
    if not actual_emergencies:
        return 1.0
    detected = [
        result
        for result in actual_emergencies
        if result.predicted_emergency
    ]
    return len(detected) / len(
        actual_emergencies
    )

def calculate_emergency_specificity(
    results: list[EvaluationResult]) -> float:

    actual_non_emergencies = [
        result
        for result in results
        if not result.expected_emergency
    ]
    if not actual_non_emergencies:
        return 1.0
    correctly_rejected = [
        result
        for result in actual_non_emergencies
        if not result.predicted_emergency
    ]
    return len(correctly_rejected) / len(
        actual_non_emergencies
    )


def count_false_negatives(
    results: list[EvaluationResult]) -> int:
    return sum(
        result.false_negative
        for result in results
    )

def count_false_positives(
    results: list[EvaluationResult]) -> int:

    return sum(
        result.false_positive
        for result in results
    )