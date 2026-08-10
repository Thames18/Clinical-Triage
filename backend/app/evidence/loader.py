import json
from pathlib import Path
from app.evidence.schemas import EvidenceSource

def load_sources(
    path: str
) -> list[EvidenceSource]:

    source_path = Path(path)
    with source_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)
    return [
        EvidenceSource(**source)
        for source in data
    ]