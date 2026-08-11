from __future__ import annotations
import os

APP_VERSION = os.getenv("APP_VERSION", "2.2.0")
MODEL_NAME = os.getenv("MODEL_NAME", "openai")
MODEL_VERSION = os.getenv("MODEL_VERSION", "unknown")
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "clinical-triage-v2")
EVIDENCE_CORPUS_VERSION = os.getenv("EVIDENCE_CORPUS_VERSION", "unversioned")

def version_info() -> dict[str, str]:
    return {
        "app_version": APP_VERSION,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "prompt_version": PROMPT_VERSION,
        "evidence_corpus_version": EVIDENCE_CORPUS_VERSION,
    }
