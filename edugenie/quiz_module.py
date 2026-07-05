from __future__ import annotations

import json
import random
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
    clean_topic = " ".join(topic.strip().split()) or "this topic"
    templates = [
        {
            "question": f"What is the main idea of {clean_topic}?",
            "options": [
                f"The basic concept of {clean_topic}",
                "A random unrelated topic",
                "Only a historical date",
                "A type of entertainment",
            ],
            "correct_answer": f"The basic concept of {clean_topic}",
        },
        {
            "question": f"Why is {clean_topic} useful to learn?",
            "options": [
                "It helps understand and solve related problems",
                "It has no practical use",
                "It is only for memorization",
                "It replaces all other subjects",
            ],
            "correct_answer": "It helps understand and solve related problems",
        },
        {
            "question": f"What is a good first step when studying {clean_topic}?",
            "options": [
                "Learn the definition and one simple example",
                "Skip the basics",
                "Memorize without understanding",
                "Avoid practice questions",
            ],
            "correct_answer": "Learn the definition and one simple example",
        },
        {
            "question": f"How can you remember {clean_topic} better?",
            "options": [
                "Practice with examples and explain it in your own words",
                "Read it once and stop",
                "Ignore mistakes",
                "Only copy notes",
            ],
            "correct_answer": "Practice with examples and explain it in your own words",
        },
        {
            "question": f"Which method is best for revising {clean_topic}?",
            "options": [
                "Short notes, examples, and quick self-tests",
                "Studying without breaks",
                "Only watching unrelated videos",
                "Guessing answers",
            ],
            "correct_answer": "Short notes, examples, and quick self-tests",
        },
    ]
    random.shuffle(templates)
    return templates[: max(1, min(question_count, len(templates)))]

