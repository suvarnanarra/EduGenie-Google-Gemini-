from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def generate_quiz(topic: str, question_count: int = 5, prefer_fast: bool = False) -> str:
    prompt = f"Generate {question_count} quiz questions about '{topic}'."
    adapter = router.select_model("quiz_generation", prefer_fast=prefer_fast)
    return adapter.generate(prompt)
