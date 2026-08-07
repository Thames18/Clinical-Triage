from app.clinical.models import MissingInformation

def calculate_uncertainty(
    missing_information: list[MissingInformation] ) -> float:
    uncertainty = 0.0

    for item in missing_information:
        if item.priority == "critical":
            uncertainty += 0.40
        elif item.priority == "high":
            uncertainty += 0.20
        else:
            uncertainty += 0.05
    return min(uncertainty, 1.0)