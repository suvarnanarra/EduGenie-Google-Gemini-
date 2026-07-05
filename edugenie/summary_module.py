from __future__ import annotations

import re

from .router import ModelRouter

router = ModelRouter()


def summarize_text(text: str, prefer_fast: bool = False) -> str:
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return "Please enter text to summarize."

    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]
    if len(sentences) >= 2:
        return "Summary: " + " ".join(sentences[:2])

    words = cleaned.split()
    if len(words) > 28:
        return "Summary: " + " ".join(words[:28]) + "..."

    return f"Summary: The main idea is about {cleaned}."
