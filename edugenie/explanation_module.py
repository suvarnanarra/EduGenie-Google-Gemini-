from __future__ import annotations

from .router import ModelRouter

router = ModelRouter()


def explain_concept(concept: str, detail: str = "", prefer_fast: bool = False) -> str:
    prompt = (
        "You are an educational AI tutor. Explain the concept clearly and simply for a beginner. "
        "Use plain language, short paragraphs, and one concrete example if helpful.\n\n"
        f"Concept: {concept}"
    )
    if detail:
        prompt += f"\nAdditional detail: {detail}"

    adapter = router.select_model("concept_explanation", prefer_fast=prefer_fast)
    response = adapter.generate(prompt)
    return response.strip() or "I could not generate an explanation for that concept right now."
