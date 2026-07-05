from __future__ import annotations

import json
import re
from typing import Any

from .router import ModelRouter

router = ModelRouter()


def _clean_json_block(response: str) -> str:
    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def generate_quiz(topic: str, question_count: int = 5, prefer_fast: bool = False) -> list[dict[str, Any]]:
    prompt = (
        f"Generate {question_count} multiple-choice quiz questions about '{topic}'. "
        "Return valid JSON as a Python list of objects. Each object must include: "
        "'question' (string), 'options' (a list of 4 strings), and 'correct_answer' (string)."
    )
    adapter = router.select_model("quiz_generation", prefer_fast=prefer_fast)
    response = adapter.generate(prompt)

    try:
        cleaned = _clean_json_block(response)
        data = json.loads(cleaned)
        if isinstance(data, dict):
            data = [data]
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
    except (TypeError, ValueError, json.JSONDecodeError):
        pass

    return []
