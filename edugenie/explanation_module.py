from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def explain_concept(concept: str, detail: str = "", prefer_fast: bool = False) -> str:
    prompt = f"Explain the concept of '{concept}' in simple, beginner-friendly language."
    if detail:
        prompt += f"\nAdditional detail: {detail}"

    adapter = router.select_model("concept_explanation", prefer_fast=prefer_fast)
    return adapter.generate(prompt)
