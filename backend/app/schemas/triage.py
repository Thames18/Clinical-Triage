from pydantic import BaseModel
from typing import List


class PatientInput(BaseModel):

    age: int

    temperature: float

    heart_rate: int

    blood_pressure: str

    oxygen_level: int

    symptoms: List[str]