from __future__ import annotations

import json
import re
from typing import Any

from .router import ModelRouter

router = ModelRouter()

def _parse_quiz_payload(response: str) -> list[dict[str, Any]]:
    if not response:
        return []

    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json|javascript|python)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
        if not match:
            return []
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError:
            return []

    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)]
    if isinstance(parsed, dict):
        return [parsed]
    return []


def generate_quiz(topic: str, question_count: int = 5, prefer_fast: bool = False) -> list[dict[str, Any]]:
    prompt = f"Generate {question_count} quiz questions about '{topic}'."
    adapter = router.select_model("quiz_generation", prefer_fast=prefer_fast)
    response = adapter.generate(prompt)
    return _parse_quiz_payload(response)

