import json
import os

from openai import OpenAI

from app.ai.prompts import (
    PROMPT_VERSION,
    SYSTEM_PROMPT,
    build_assessment_prompt,
)
from app.ai.schemas import AIClinicalAssessment
from app.evidence.schemas import RetrievedEvidence


class AIReasoningService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.prompt_version = PROMPT_VERSION

    def assess(
        self,
        patient: dict,
        evidence: list[RetrievedEvidence],
    ) -> AIClinicalAssessment:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_assessment_prompt(
                        patient,
                        [item.model_dump() for item in evidence],
                    ),
                },
            ],
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("The AI returned an empty response.")

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError("The AI returned invalid JSON.") from exc

        return AIClinicalAssessment(**parsed)
