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
    # Prefer local LaMini inference for explanations if available, otherwise use adapter
    adapter = router.select_model("concept_explanation", prefer_fast=prefer_fast)
    try:
        return adapter.generate(prompt)
    except Exception:
        # As a last resort, call the cloud adapter
        return adapter.generate(prompt)
