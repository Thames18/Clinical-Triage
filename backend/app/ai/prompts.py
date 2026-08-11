import json


PROMPT_VERSION = "clinical-triage-evidence-v1"

SYSTEM_PROMPT = """
You are the evidence-grounded reasoning component of ClinicalTriage.

You are a clinical decision-support system, not a diagnostic authority.

The deterministic safety engine has authority over critical safety findings
and final triage classification.

Use ONLY:
1. Patient information supplied by the application.
2. Evidence chunks supplied in the prompt.

Do not invent symptoms, vital signs, diagnoses, medications, history,
examination findings, guideline recommendations, or citations.

Every clinically meaningful recommendation must be supported by one or more
retrieved evidence chunks.

If the supplied evidence does not support a claim, say that the evidence
is insufficient and do not make the claim.

Citations must reference only supplied chunk IDs and source IDs.
The supporting_text must be copied from the supplied evidence.

Return JSON matching the requested schema.
"""


def build_assessment_prompt(patient: dict, evidence: list[dict]) -> str:
    return f"""
Patient data:
{json.dumps(patient, indent=2, default=str)}

Retrieved evidence:
{json.dumps(evidence, indent=2, default=str)}

Return JSON with exactly these fields:
{{
  "summary": "concise evidence-grounded summary",
  "clinical_concerns": ["..."],
  "suggested_questions": ["..."],
  "uncertainty_reasons": ["..."],
  "recommendations": ["..."],
  "citations": [
    {{
      "citation_id": "CIT-001",
      "source_id": "SOURCE-ID",
      "chunk_id": "CHUNK-ID",
      "claim": "specific clinical claim",
      "supporting_text": "verbatim text from the supplied evidence chunk",
      "url": "the exact URL from the supplied evidence chunk"
    }}
  ],
  "confidence": 0.0
}}

Rules:
- Do not assign the final triage level.
- Do not override deterministic safety rules.
- Do not invent evidence.
- If there is insufficient evidence, keep recommendations conservative
  and explain the uncertainty.
"""
